def extra_process(raw_data: dict) -> list:
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

    # 将工矿1C数据合并到GK1C
    if gongkuang_key and gongkuang_key in raw_data:
        gongkuang_items = raw_data.pop(gongkuang_key)
        for item in gongkuang_items:
            item["id"] = "GK1C-" + item["id"].split("-")[-1]
        raw_data.setdefault(gk1c_key, []).extend(gongkuang_items)

    # 删除车号未知
    if unknown_key and unknown_key in raw_data:
        raw_data.pop(unknown_key)

    # 展平为列表
    result = []
    for items in raw_data.values():
        result.extend(items)
    return result
# 让Agent写的，懒了