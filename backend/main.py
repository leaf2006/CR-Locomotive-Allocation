import asyncio
import orjson
from fetch import first_web_fetch, web_fetch
from pathlib import Path
from utils import utils
async def main():
    print("开始获取下关站所有数据...\n")
    current_dir = Path(__file__).parent
    fetch_path = current_dir / "fetch_url.json"
    data_dir = current_dir.parent / "data"
    raw_result_path = data_dir / "raw_result.json"

    with open(fetch_path, "rb") as fetch_f:
        content = fetch_f.read()
        fetch_url = orjson.loads(content)
    first_fetch_result, store_dict = await first_web_fetch(fetch_url) # 首次网络请求，将会获取后续所有网络请求所需的url
    print(store_dict)

    print("等待三秒...")
    await asyncio.sleep(3)
    
    raw_result = await web_fetch(store_dict, first_fetch_result)
    print("数据获取已完成，正在进行去重...")
    raw_result = utils.remove_duplicate_data(raw_result)
    print("去重完成，正在进行写入...")
    write_first_fetch_result = orjson.dumps(
        raw_result,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
    )
    with open(raw_result_path, 'wb') as result_f:
        result_f.write(write_first_fetch_result)
    print("写入已完成！")

if __name__ == "__main__":
    asyncio.run(main())