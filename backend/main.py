import asyncio
import orjson
from fetch import index_first_web_fetch
# from utils import result_data_initialization
from pathlib import Path
async def main():
    print("开始获取下关站所有数据...\n")
    current_dir = Path(__file__).parent
    fetch_path = current_dir / "fetch_url.json"
    data_dir = current_dir.parent / "data"
    raw_result_path = data_dir / "raw_result.json"

    with open(fetch_path, "rb") as fetch_f:
        content = fetch_f.read()
        fetch_url = orjson.loads(content)
    first_fetch_result, detail_fetch_urls = await index_first_web_fetch(fetch_url)
    print("首次数据获取已完成，正在进行写入...")
    write_first_fetch_result = orjson.dumps(
        first_fetch_result,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
    )
    with open(raw_result_path, 'wb') as result_f:
        result_f.write(write_first_fetch_result)
    print("写入已完成！")

if __name__ == "__main__":
    asyncio.run(main())