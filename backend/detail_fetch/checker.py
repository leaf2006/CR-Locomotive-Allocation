import orjson
import asyncio
from pathlib import Path
import detail_main
from utils import utils

async def main():
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent.parent / "data"
    divide_path = data_dir / "divide.json"
    raw_result_path = data_dir / "raw_result.json"

    with open(raw_result_path, 'rb') as raw_result_f:
        raw_result = orjson.loads(raw_result_f.read())    
    raw_result = utils.remove_duplicate_data(raw_result)
    write_raw_result = orjson.dumps(
        raw_result,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
    )
    with open(raw_result_path, "wb") as raw_result_f:
        raw_result_f.write(write_raw_result)
    print("[SUCCESS] 去重完成") # 这个程序一般不用，用的时候数据多少有点问题。所以这里再加一个去重


    unfetch_list = utils.find_items_need_detail(raw_result)
    if not unfetch_list:
        print("[SUCCESS] 数据完整，程序结束")
    else:
        print(f"[INFO] 共有{len(unfetch_list)}项数据因异常而未进行网络请求，正在重新进行网络请求...")
        write_divide = orjson.dumps(
            unfetch_list,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
        )
        with open(divide_path, "wb") as divide_f:
            divide_f.write(write_divide) # 如果程序重启，这一部分也能存储，最后按照正常的fetch流程来。
        await detail_main.main()

if __name__ == "__main__":
    asyncio.run(main())
