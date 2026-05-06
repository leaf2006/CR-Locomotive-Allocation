import orjson
import asyncio
from pathlib import Path
import httpx
from format import get_webfetch_data, normal_format_data
from utils import utils

# def fetch_divide(raw_data :list, store :list) -> list:
#     for i in range(0, len(raw_data), 10):
#         batch = raw_data[i:i+10]
#         store.append(batch)
async def _first_normal_data_processing(
        client: httpx.AsyncClient,
        url: str ,
        store_dict :list,
        first_raw_result :list,
        # semaphore,
) -> str:
    # async with semaphore:
    index_response = await client.post(url)
    index_response.encoding = "gb2312"
    # detail_fetch_urls = get_webfetch_data(index_response.text, "normal_fetch", url, store_dict, first_raw_result, detail_fetch_urls)
    get_webfetch_data(index_response.text, "normal_fetch", url, store_dict, first_raw_result)

async def _normal_data_processing(client: httpx.AsyncClient, url: str, raw_result :list):
    response = await client.post(url)
    response.encoding = "gb2312"
    normal_format_data(response.text, "normal_fetch", raw_result)

# async def _train_detail_processing(
#         client: httpx.AsyncClient,
#         url :str,
#         first_raw_result :list
# ):
#     response = await client.post(url)
#     response.encoding = "gb2312"
#     get_detail_data(response.text, first_raw_result)
async def _special_fetch_groupA_data_processing(client: httpx.AsyncClient, url: str, store_dict :list) -> str:
    response = await client.post(url)
    response.encoding = "gb2312"
    get_webfetch_data(response.text, "special_fetch_group_A", url, store_dict)
    

async def index_first_web_fetch(fetch_url) -> list[str]:
    raw_url = fetch_url['xiaguanzhan_url']
    normal_fetch = fetch_url["normal_fetch"]
    special_fetch_group_A = fetch_url['special_fetch_group_A']
    special_fetch_group_B = fetch_url['special_fetch_group_B']
    special_fetch_DF11Z = fetch_url['special_fetch_DF11Z']
    # semaphore = asyncio.Semaphore(10)
    store_dict = {
        "normal_fetch":[],
        "special_fetch_group_A":[],
        "special_fetch_group_B":[],
        "special_fetch_group_DF11Z":[]
    }
    first_raw_result = {}
    async with httpx.AsyncClient(timeout=30.0) as client:
        # tasks = [
        #     _fetch_one(client, f"{raw_url}{trains}-3.asp")
        #     for trains in normal_fetch
        # ]
        batches = [] # 分组处理

        utils.fetch_divide(normal_fetch, batches)

        # tasks = []

        # for batch in batches:
        #     for trains in batch:
        #         coro = _first_normal_data_processing(client, f"{raw_url}{trains}-3.asp", store_dict, first_raw_result, detail_fetch_urls, semaphore)
        #         tasks.append(coro)  
        for batch in batches:
            tasks = []
            for trains in batch:
                coro = _first_normal_data_processing(client, f"{raw_url}{trains}-3.asp", store_dict, first_raw_result)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # 每批之间等 1 秒

        # await asyncio.gather(*tasks) # 异步并发执行
    # async with httpx.AsyncClient(timeout=30.0) as client:
    #     batches = []
    #     utils.fetch_divide(special_fetch_group_A, batches)

    #     tasks = []
    #     for batch in batches:
    #         for trains in batch:
    #             coro = _special_fetch_groupA_data_processing(client, f"{raw_url}soso.asp?keyword={trains}", store_dict)
    #             tasks.append(coro)
    #     await asyncio.gather(*tasks)

    # return list(data)
    return first_raw_result, store_dict

async def web_fetch(url_dict: list, raw_result :list) -> list[str]:
    normal_url_dict = url_dict['normal_fetch']
    async with httpx.AsyncClient(timeout=30.0) as client:
        batches = []
        utils.fetch_divide(normal_url_dict, batches)
        for batch in batches:
            tasks = []
            for url in batch:
                coro = _normal_data_processing(client, url, raw_result)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
    
    return raw_result

