import orjson
import asyncio
from pathlib import Path
import httpx
from format import get_webfetch_data

def fetch_divide(raw_data :list, store :list) -> list:
    for i in range(0, len(raw_data), 10):
        batch = raw_data[i:i+10]
        store.append(batch)
async def _first_normal_data_processing(client: httpx.AsyncClient, url: str ,store_dict :list) -> str:
    response = await client.post(url)
    response.encoding = "gb2312"
    get_webfetch_data(response.text, True, url, store_dict)
    # return response.text

async def first_normal_fetch(fetch_url) -> list[str]:
    raw_url = fetch_url['xiaguanzhan_url']
    normal_fetch = fetch_url["normal_fetch"]
    async with httpx.AsyncClient(timeout=30.0) as client:
        # tasks = [
        #     _fetch_one(client, f"{raw_url}{trains}-3.asp")
        #     for trains in normal_fetch
        # ]
        batches = [] # 分组处理

        fetch_divide(normal_fetch, batches)

        tasks = []
        store_dict = []
        for batch in batches:
            for trains in batch:
                coro = _first_normal_data_processing(client, f"{raw_url}{trains}-3.asp", store_dict)
                tasks.append(coro)  
            
        # for trains in normal_fetch:
        #     coro = _fetch_one(client, f"{raw_url}{trains}-3.asp")
        #     tasks.append(coro)

        await asyncio.gather(*tasks) # 异步并发执行
    # return list(data)
    return store_dict
        


