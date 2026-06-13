from pathlib import Path
import orjson
import re
import httpx
import asyncio

# def result_data_initialization():
#     current_dir = Path(__file__).parent
#     data_dir = current_dir.parent / "data"
#     raw_result_path = data_dir / "raw_result.json"

class utils:
    def fetch_divide(raw_data :list, store :list) -> list:
        """将所有数据分为十个一组"""
        for i in range(0, len(raw_data), 10):
            batch = raw_data[i:i+10]
            store.append(batch)
    def xiaguanzhan_first_match(pattern, text):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else None
    
    def split_raw_result(raw_result: dict, chunk_size: int = 100) -> list:
        """将 raw_result 展平为小项 list，按 chunk_size 分块。每个 item 注入 train_series 字段。"""
        # FIX: 展平 dict 为 list，去掉车型层级，每个 item 注入 train_series 保留归属
        all_items = []
        for train_series, train_list in raw_result.items():
            for item in train_list:
                pro_id = item.get('pro_id', '') # 修改为更安全的pro_id获取方式
                if pro_id == "":
                    continue # 如果pro_id为空，则直接跳过
                item['train_series'] = train_series
                all_items.append(item)

        # FIX: 按 chunk_size 切片，返回 list[list[dict]] 而非 list[dict]
        return [all_items[i:i + chunk_size] for i in range(0, len(all_items), chunk_size)]
    
    def remove_duplicate_data(raw_result: dict) -> dict:
        """删除重复数据，遍历每个机型下的列表，按 (id, allocation) 去重，保留首个条目。"""
        for key in raw_result:
            seen = set()
            deduped = []
            for item in raw_result[key]:
                pair = (item.get("id"), item.get("allocation"))
                if pair not in seen:
                    seen.add(pair)
                    deduped.append(item)
            raw_result[key] = deduped
        return raw_result

    def find_items_need_detail(raw_result: dict) -> list:
        """找出有pro_id但缺少photo_url、photo_date、photo_author与manufacturer的条目，按每100组分批。"""
        needs_detail = []
        required_fields = ["photo_url", "photo_date", "photo_author", "manufacturer"]

        for _, items in raw_result.items():
            for item in items:
                has_pro_id = "pro_id" in item and item["pro_id"] != ""
                if has_pro_id and all(field not in item for field in required_fields):
                    needs_detail.append(item)

        batch_size = 100
        return [needs_detail[i:i + batch_size] for i in range(0, len(needs_detail), batch_size)]

async def run_with_retry(coro_factory, *, max_retries=3, base_delay=2.0):
    """当出现网络问题时，程序自动进行三次重连"""
    for attempt in range(1, max_retries + 1):
        try:
            return await coro_factory()
        except (httpx.ReadTimeout, httpx.RemoteProtocolError) as exc:
            if attempt == max_retries:
                raise
            wait = base_delay * (2 ** (attempt - 1))
            print(f"fetch failed: {exc}. retry in {wait}s (attempt {attempt}/{max_retries})")
            await asyncio.sleep(wait)
