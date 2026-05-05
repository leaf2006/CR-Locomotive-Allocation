import asyncio
import re
import httpx
from utils import utils
from format import get_detail_data
async def _train_detail_processing(
        client: httpx.AsyncClient,
        url :str,
        first_raw_result :list,
        semaphore
):
    async with semaphore:
        response = await client.post(url)
        response.encoding = "gb2312"
        print(f"已请求：{url}")
        get_detail_data(response.text, first_raw_result)
async def detail_web_fetch(fetch_url :list, first_raw_result :list) -> list[str]:
    semaphore = asyncio.Semaphore(10)
    async with httpx.AsyncClient(timeout=30.0) as client:
        batches = []
        utils.fetch_divide(fetch_url, batches)

        # tasks = []

        for batch in batches:
            tasks = []
            for detail_url in batch:
                coro = _train_detail_processing(client, detail_url, first_raw_result, semaphore)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
        # await asyncio.gather(*tasks)
