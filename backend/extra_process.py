def extra_process(raw_data: dict) -> dict:
    """对于数据的附加的个性化处理

    1. 将"工矿1C"数据的id从"工矿1C-XXXX"改为"GK1C-XXXX"，并合并到GK1C中
    2. 删除"车号未知"代码块
    """
    gk1c_key = "GK1C"
    gongkuang_key = None
    unknown_key = None

    for key in raw_data:
        if key == gk1c_key:
            continue
        if "工矿" in key and "1C" in key:
            gongkuang_key = key
        if "车号未知" in key:
            unknown_key = key

    result = {}
    for key, items in raw_data.items():
        if key == unknown_key or key == gongkuang_key:
            continue
        if key == gk1c_key:
            merged = list(items)
            if gongkuang_key and gongkuang_key in raw_data:
                for item in raw_data[gongkuang_key]:
                    new_item = dict(item)
                    new_item["id"] = "GK1C-" + new_item["id"].split("-")[-1]
                    merged.append(new_item)
            result[key] = merged
        else:
            result[key] = list(items)

    return result
