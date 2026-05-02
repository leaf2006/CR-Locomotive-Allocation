import asyncio
import orjson
from fetch import first_normal_fetch

from pathlib import Path
async def main():
    print("开始获取下关站所有数据...\n")

    current_dir = Path(__file__).parent
    file_path = current_dir / "fetch_url.json"
    with open(file_path, "rb") as f:
        content = f.read()
        fetch_url = orjson.loads(content)

        data = await first_normal_fetch(fetch_url)
        print(data)
    

if __name__ == "__main__":
    asyncio.run(main())