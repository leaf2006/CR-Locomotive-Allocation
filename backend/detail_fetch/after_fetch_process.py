import orjson
import re
import asyncio
from pathlib import Path

async def main():
    """为保证灵活性可单独运行"""
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent.parent / "data"
    raw_result_path = data_dir / "raw_result.json"
    fix_path = data_dir / "fix.json"
    with open(raw_result_path, 'rb') as raw_result_f:
        raw_result = orjson.loads(raw_result_f.read())
    
    print("[SUCCESS] raw_result.json已获取，正在进行数据规范化处理...")
    result = after_fetch_process(raw_result)
    print("[SUCCESS] 处理完成，正在写入...")
    write_result = orjson.dumps(
        result,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2
    )
    if write_result:
        with open(raw_result_path, 'wb') as result_f:
            result_f.write(write_result)


def _strip_html_tags(text: str) -> str:
    """去除字符串中的HTML标签，如<FONT face=Verdana>...</FONT>"""
    return re.sub(r"<[^>]+>", "", text)


# 硬编码的厂商别名
_MANUFACTURER_ALIASES = {
    "浦镇": "中车南京浦镇",
    "四方": "中车青岛四方",
    "中车青岛四方客车": "中车青岛四方",
    "青岛庞巴迪": "四方庞巴迪",
}


def _normalize_single_manufacturer(raw_name: str, normal_manufacturer: dict) -> str:
    """将单个厂商名标准化，优先 keyword 匹配，其次硬编码别名，否则原样返回。"""
    for keyword, normalized_full_name in normal_manufacturer.items():
        if keyword in raw_name:
            return normalized_full_name
    return _MANUFACTURER_ALIASES.get(raw_name, raw_name)


def after_fetch_process(raw_result: dict) -> dict:
    """在所有请求完后，对数据进行规整与修身"""
    current_dir = Path(__file__).parent
    curated_path = current_dir.parent / "curated.json"
    with open(curated_path, 'rb') as curated_f:
        curated_data = orjson.loads(curated_f.read())

    fix_path = current_dir.parent.parent / "data" / "fix.json"
    with open(fix_path, 'rb') as fix_f:
        fix_data = orjson.loads(fix_f.read())

    # 1. 先进行名称处理 —— 去除残留的HTML标签
    for series_items in raw_result.values():
        for item in series_items:
            if "manufacturer" in item:
                item['manufacturer'] = _strip_html_tags(item['manufacturer']).strip()
            if "allocation" in item:
                item['allocation'] = _strip_html_tags(item['allocation']).strip()
            if "photo_author" in item:
                item["photo_author"] = _strip_html_tags(item["photo_author"]).strip()
            if "photo_date" in item:
                item['photo_date'] = _strip_html_tags(item['photo_date']).strip()
    
    # 2. 进行厂家名的统一化
    normal_manufacturer = curated_data['normal_manufacturer']
    for series_items in raw_result.values():
        for item in series_items:
            if 'manufacturer' not in item:
                continue
            raw_manufacturer = item['manufacturer']
            parts = raw_manufacturer.split('/')
            normalized_parts = [_normalize_single_manufacturer(p.strip(), normal_manufacturer) for p in parts]
            item['manufacturer'] = '/'.join(normalized_parts)
    
    # 3. 进行配属名的去重
    standard_allocation_name = curated_data['standard_allocation_name'] # 标准化配属名
    for series_items in raw_result.values():
        for item in series_items:
            if 'allocation' not in item:
                continue
            allocation_name = item['allocation']
            matched = False
            for standard_name, raw_name_list in standard_allocation_name.items():
                for raw_name in raw_name_list:
                    if raw_name == allocation_name: # allocation匹配到了非标准值
                        item['allocation'] = standard_name
                        matched = True
                        break
                if matched:
                    break
    
    # 4.将fix.json中的数据写入raw_result
    for fix_item in fix_data:
        series = fix_item['train_series']
        fix_id = fix_item['id']
        if series not in raw_result:
            raw_result[series] = [fix_item]
            continue
        matched = False
        for i, item in enumerate(raw_result[series]):
            if item.get('id') == fix_id:
                raw_result[series][i] = fix_item
                matched = True
                break
        if not matched:
            raw_result[series].append(fix_item)

    return raw_result


if __name__ == "__main__":
    asyncio.run(main())
