import orjson
import asyncio
from pathlib import Path
import httpx
from format import get_webfetch_data, format_data
from utils import utils

async def _first_normal_data_processing(client: httpx.AsyncClient, url: str, store_dict :list, first_raw_result :list) -> str:
    """发起首次normal_fetch的网络请求，并把请求结果引入数据处理部分"""
    response = await client.post(url)
    response.encoding = "gb2312"
    get_webfetch_data(response.text, "normal_fetch", url, store_dict, first_raw_result)

async def _normal_data_processing(client: httpx.AsyncClient, url: str, raw_result :list):
    """发起后续normal_fetch的网络请求，并把结果引入数据处理部分"""
    response = await client.post(url)
    response.encoding = "gb2312"
    format_data(response.text, "normal_fetch", raw_result)

async def _first_special_data_processing(client: httpx.AsyncClient, url: str, store_dict :list, first_raw_result :list) -> str:
    """发起首次special_fetch的网络请求，并把请求结果引入数据处理部分"""
    response = await client.post(url)
    response.encoding = "gb2312"
    get_webfetch_data(response.text, "special_fetch", url, store_dict, first_raw_result)

async def _special_data_processing(client: httpx.AsyncClient, url: str, raw_result :list):
    """发起后续special_fetch的网络请求，并把结果引入数据处理部分"""
    response = await client.post(url)
    response.encoding = "gb2312"
    format_data(response.text, "special_fetch", raw_result)

async def _first_emu_normal_data_processing(client: httpx.AsyncClient, url: str, store_dict: list, first_raw_result: list):
    """发起首次emu_normal_fetch的网络请求，并把请求结果引入数据处理部分"""
    response = await client.get(url)
    # response.encoding = "gb2312"
    get_webfetch_data(response.text, "emu_normal_fetch", url, store_dict, first_raw_result)

async def _emu_normal_data_processing(client: httpx.AsyncClient, url: str, raw_result :list):
    """发起后续emu_normal_fetch的网络请求，并把结果引入数据处理部分"""
    response = await client.get(url)
    # response.encoding = "gb2312"
    format_data(response.text, "emu_normal_fetch", raw_result)

async def first_web_fetch(fetch_url) -> list[str]:
    """首次网络请求"""
    raw_url = fetch_url['xiaguanzhan_url']
    raw_emu_url = fetch_url['emu_url']
    normal_fetch = fetch_url["normal_fetch"]
    special_fetch = fetch_url["special_fetch"].values()
    emu_normal_fetch = list(fetch_url['emu_normal_fetch'].keys())
    emu_normal_fetch_xiaguan = fetch_url['emu_normal_fetch'].values()
    emu_special_fetch = fetch_url['emu_special_fetch']
    # semaphore = asyncio.Semaphore(10)
    store_dict = {
        "normal_fetch":[],
        "special_fetch":[],
        "emu_normal_fetch": [],
        "emu_normal_fetch_xiaguan": [],
        "emu_special_fetch": []
    }
    first_raw_result = {}
    
    # normal_fetch
    async with httpx.AsyncClient(timeout=30.0) as client:
        batches = [] # 分组处理
        utils.fetch_divide(normal_fetch, batches) 

        for batch in batches:
            tasks = []
            for trains in batch:
                coro = _first_normal_data_processing(client, f"{raw_url}{trains}-3.asp", store_dict, first_raw_result)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # 每批之间等 1 秒
    
    print("[SUCCESS]normal_fetch组首次请求已完成")
    print("[INFO]等待冷却三秒，进行special_fetch组的首次请求...")
    await asyncio.sleep(3)

    # special_fetch
    async with httpx.AsyncClient(timeout=30.0) as client:
        # batches = []
        # 因为没有几组，所以可以一起放进去请求，不需要分组
        print(special_fetch)
        tasks = []
        for url in special_fetch:
            coro = _first_special_data_processing(client, url, store_dict, first_raw_result)
            tasks.append(coro)
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)
    
    print("[SUCCESS]special_fetch组首次请求已完成")
    print("[INFO]等待冷却三秒，进行emu_normal_fetch组的首次请求...")

    # emu_normal_fetch
    async with httpx.AsyncClient(timeout=30.0) as client:
        batches= []
        print(emu_normal_fetch)
        utils.fetch_divide(emu_normal_fetch, batches)

        for batch in batches:
            tasks = []
            for emu in batch:
                coro = _first_emu_normal_data_processing(client, f"{raw_emu_url}{emu}", store_dict, first_raw_result)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
        

    return first_raw_result, store_dict

async def web_fetch(url_dict: list, raw_result :list) -> list[str]: # url_dict对应上面的store_dict
    """后续常规网络请求"""
    normal_url_dict = url_dict['normal_fetch']
    special_url_dict = url_dict['special_fetch']
    emu_normal_url_dict = url_dict['emu_normal_fetch']

    # normal_fetch
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
    print("[SUCCESS]normal_fetch组请求已完成")
    print("[INFO]等待冷却三秒，进行special_fetch组的请求...")
    await asyncio.sleep(3)   

    # special_fetch
    async with httpx.AsyncClient(timeout=30.0) as client:
        batches = []
        utils.fetch_divide(special_url_dict, batches)
        for batch in batches:
            tasks = []
            for url in batch:
                coro = _special_data_processing(client, url, raw_result)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
    print("[SUCCESS]special_fetch组请求已完成")
    print("[INFO]等待冷却三秒，进行emu_normal_fetch组的请求...")
    await asyncio.sleep(3)

    # emu_normal_fetch
    async with httpx.AsyncClient(timeout=30.0) as client:
        batches = []
        utils.fetch_divide(emu_normal_url_dict, batches)

        for batch in batches:
            tasks = []
            for url in batch:
                coro = _emu_normal_data_processing(client, url, raw_result)
                tasks.append(coro)
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
    
    return raw_result

