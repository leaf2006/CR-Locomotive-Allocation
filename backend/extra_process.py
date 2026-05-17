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
def compare_and_add_proid(emu_xiaguan_compare: dict, raw_data: dict) -> dict:
    """把下关站获取的对应动车组车号pro_id合并到raw_data中

    用emu_xiaguan_compare中所有大类里小类的"id"去比对raw_data中的"id"，
    匹配到的就将emu_xiaguan_compare里的"pro_id"赋值给raw_data中的对应项。
    """
    # 构建 id -> pro_id 查找表
    id_to_pro_id: dict[str, str] = {}
    for items in emu_xiaguan_compare.values():
        for item in items:
            if "id" in item and "pro_id" in item:
                id_to_pro_id[item["id"]] = item["pro_id"]

    # 遍历 raw_data，匹配并赋值 pro_id
    for items in raw_data.values():
        for item in items:
            if item.get("id") in id_to_pro_id:
                item["pro_id"] = id_to_pro_id[item["id"]]

    return raw_data

