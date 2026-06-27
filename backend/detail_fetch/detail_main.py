import os
import asyncio
import orjson
import httpx
import sys
import random
from pathlib import Path
from datetime import datetime
from detail_format import format_data
from after_fetch_process import after_fetch_process
from utils import utils, run_with_retry

URL = "http://www.xiaguanzhan.com/ProView.asp?ProId="
async def _timeout_exit(seconds: float, progress: dict):
    """异步计时器，到期后保存进度并强制退出程序"""
    await asyncio.sleep(seconds)
    print(f"[ERROR] 程序运行已超过 {seconds / 3600:.1f} 小时，正在保存进度后退出...")
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent.parent / "data"
    backup_path = data_dir / "backup.json"
    backup = { "page": int(progress["page"]) }
    write_backup = orjson.dumps(
        backup,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
    )
    with open(backup_path, 'wb') as backup_f:
        backup_f.write(write_backup)
    print(f"[SUCCESS] 进度已保存（page={progress['page']}），程序退出")
    os._exit(1)  # 绕过 asyncio 事件循环，直接终止进程

async def main():
    progress = {"page": 0}
    # 启动5.5小时超时计时器
    timeout_task = asyncio.create_task(_timeout_exit(5.5 * 3600, progress))

    try:
        await _main_logic(progress)
    finally:
        if not timeout_task.done():
            timeout_task.cancel()

async def _main_logic(progress: dict):
    # 读取所有本地数据
    print("[INFO] 开始获取下关站详细数据...\n正在获取raw_result.json...")
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent.parent / "data"
    raw_result_path = data_dir / "raw_result.json"
    backup_path = data_dir / "backup.json"
    divide_path = data_dir / "divide.json"
    version_path = data_dir / "version.txt"

    with open(raw_result_path, "rb") as raw_result_f, open(backup_path, "rb") as backup_f, open(divide_path, "rb") as divide_f:
        raw_result = orjson.loads(raw_result_f.read())
        backup_data = orjson.loads(backup_f.read())
        fetch_list = orjson.loads(divide_f.read())
    print("[SUCCESS] raw_result.json已获取")

    # 首次启动程序，divide.json内无内容，则在里面写入分组后的数据
    if not fetch_list:
        print("[INFO] 程序为首次启动，并未将数据分组，正在进行分组...")
        fetch_list = utils.split_raw_result(raw_result)
        write_divide = orjson.dumps(
            fetch_list,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
        )
        with open(divide_path, "wb") as divide_f:
            divide_f.write(write_divide) # 写入，如果程序要重启直接用这里的
    else:
        print("[SUCCESS] 已有分组数据，无需重新分组")

    rerun_sum = len(fetch_list)
    print(f"[SUCCESS] 分组完成，将进行{rerun_sum}组查询\n [INFO] 正在进行网络请求步骤...")
    
    # 读取backup.json，如果backup内的page有值，则从那个page开始fetch
    if backup_data.get('page','') == "":
        count = 0
        progress["page"] = 0
    else:
        count = backup_data.get('page')
        progress["page"] = count
        print(f"[INFO] 程序将从第{count +1}次继续进行网络请求...")
        await asyncio.sleep(3)

    while count < rerun_sum:
        now_raw_result = fetch_list[count] # 当前fetch请求所使用的数据

        print(f"[INFO] 正在进行第{count +1}组网络请求...")

        result = await run_with_retry(lambda: detail_fetch(now_raw_result, count))

        print("[SUCCESS] 数据获取完成，正在进行写入...")


        # Fix: id_map键从id改为(id, allocation)，避免同id不同配属的条目互相覆盖
        print(result)
        if result:
            for new_item in result:
                for train_series, raw_items in raw_result.items():
                    id_map = {(item["id"], item.get("allocation", "")): i for i, item in enumerate(raw_items)}
                    key = (new_item["id"], new_item.get("allocation", ""))
                    if key in id_map:
                        raw_items[id_map[key]] = new_item
                        break  # 找到即停

            write_result = orjson.dumps(
                raw_result,
                option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
            )
        else:
            print("[INFO] 本组无需写入（result 为空）")
            write_result = None

        # FIX: 先写数据再写进度，崩溃时不会跳过未完成的组
        if write_result:
            with open(raw_result_path, 'wb') as result_f:
                result_f.write(write_result)

        count += 1
        progress["page"] = count
        print("[SUCCESS] 当前组写入已完成！")

    print("[INFO] 所有数据处理完成，正在进行数据规范化处理...")
    with open(raw_result_path, 'rb') as raw_result_f:
        raw_result = orjson.loads(raw_result_f.read()) # 全部fetch完后的raw_result
    
    result = after_fetch_process(raw_result)

    write_result = orjson.dumps(
        result,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
    )
    if write_result:
        with open(raw_result_path, 'wb') as result_f:
            result_f.write(write_result)

    # 增加版本号写入
    print("[SUCCESS] 规整已完成\n[INFO] 正在写入版本号...")
    version = str(datetime.now().strftime("%Y%m%d"))
    with open(version_path, 'w', encoding='utf-8') as version_f:
        version_f.write(version)
    
    print("[SUCCESS] 版本号写入完成！\n[SUCCESS] 程序结束")
    
async def _data_processing(client: httpx.AsyncClient, url: str, item: dict, result: dict, page: int):  # FIX: 参数从 (train_info, raw_result) 改为 (item, result)
    """执行网络请求"""
    for retry in range(1,6):
        # 如果请求失败或响应为空，进行五次重试
        try:
            response = await client.get(url)
            response.encoding = "gb2312"
            # FIX: 检测空响应，tasks清零后第一个请求概率性拿到空body(status=200但无内容)
            if not response.text.strip():
                raise Exception(f"响应内容为空 (status={response.status_code})")
            break
        except Exception as error:
            cold_time = random.uniform(30.0,90.0)
            print(f"[WARN] 由于{str(error)}，正在尝试重新请求(第{retry}次)，冷却{cold_time:.1f}s...")
            await asyncio.sleep(cold_time)
    else:
        print("[ERROR] 出现请求错误，程序将会异常退出！除本组之外的先前组的结果已经保存，正在备份已完成的页码，以便稍后重启")
        current_dir = Path(__file__).parent
        data_dir = current_dir.parent.parent / "data"
        backup_path = data_dir / "backup.json"
        backup = { "page": int(page) }

        write_backup = orjson.dumps(
            backup,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
        )
        with open(backup_path, 'wb') as backup_f:
            backup_f.write(write_backup)

        await asyncio.sleep(3)
        sys.exit(1)

    format_data(response.text, item, result)  # FIX: 传入 item 和 result，由 format_data 整合
        

async def detail_fetch(chunk: list, page: int) -> dict:  # FIX: 参数改为扁平 list，返回值改为 dict
    """网络请求，chunk 为最多 100 个小项的扁平 list，返回以车型为 key 的 dict；page为当前页码"""
    group_count = 0 # 组计数，达到10自动触发random sleep，从0.1秒到0.9秒不等
    tasks = []
    result = []

    client = httpx.AsyncClient(
        timeout=30.0,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
    )
    try:
        for item in chunk:  # FIX: 单层遍历扁平 list，取代原来的两层嵌套
            pro_id = item.get('pro_id', '')
            # if pro_id == "":
            #     continue

            tasks.append(_data_processing(client, f"{URL}{pro_id}", item, result, page))  # FIX: 传入 item 和 result
            await asyncio.sleep(random.uniform(0.1, 0.5))
            group_count += 1
            if group_count >= 10:
                await asyncio.gather(*tasks)
                tasks.clear()
                print("本小组完成，tasks清零")
                group_count = 0
                await asyncio.sleep(1)

        # 处理剩余不足10个的任务
        if tasks:
            await asyncio.gather(*tasks)

    finally:
        await client.aclose()
        cold_time = random.uniform(60.0,180.0)
        print(f"[INFO] 冷却中，冷却{cold_time}s")
        await asyncio.sleep(cold_time) # 冷却1分钟到3分钟不等
    return result  # FIX: 返回以车型为 key 的 dict，而非原来的扁平 list

if __name__ == "__main__":
    asyncio.run(main())
