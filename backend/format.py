import orjson
import asyncio
import re
from utils import utils
# from details_fetch import web_fetch

def normal_format_data(response_text :str,fetch_status :str, raw_result :list):
    """初步获取页面的主页信息，不包括制造商与设计时速，存入dict中"""
    if fetch_status == "normal_fetch":
        normal_page_match = re.findall(r'<a class="jytb" href="ProView\.asp\?ProId=(\d+)" target="_blank">([^<]+)</a>', response_text)
        normal_page_match = [(pid, text) for pid, text in normal_page_match if any('\u4e00' <= c <= '\u9fff' for c in text)]

        print(normal_page_match)
        for detail in normal_page_match:
            # pro_id = detail[0]
            raw_train_detail = detail[1] # TODO 当录入GKD等车型时， 这边会出现错位
            raw_train_detail_split = raw_train_detail.split(' ') # 分割信息，只提取[1]：车型车号（全英文），[2]配属
            if len(raw_train_detail_split) < 3 or "-" not in raw_train_detail_split[1]:
                if "-" in raw_train_detail_split[0] and "-" not in raw_train_detail_split[1]:
                    train_series_number = raw_train_detail_split[0]
                    train_allocation = raw_train_detail_split[1] # TODO 傻逼判断法，需要后续修改
                else:
                    train_series_number = raw_train_detail_split[1]
                    train_allocation = "暂无配属"
            else:
                train_series_number = raw_train_detail_split[1]
                train_allocation = raw_train_detail_split[2] # 配属
            train_series = train_series_number.split('-')[0] # 型号

            raw_result.setdefault(train_series, []).append({
                "id": train_series_number,
                "allocation": train_allocation,
                "manufacturer": "",
                "design_speed": ""
            })
            print(f"{train_series_number}已录入，配属：{train_allocation}")

def get_webfetch_data(response_text :str, fetch_status :str, raw_url :str, store_dict :list, raw_result :list):
    """获取当前组的信息总量、总页数，顺便获取当页的信息"""
    if fetch_status == "normal_fetch": # 获取总页数，以制定所有需要fetch的url
        total_page_match = re.search(r"\[页次<Font color='Red'>1</Font>/(.*?)页\]", response_text)
        if total_page_match:
            total_page = total_page_match.group(1)

        for i in range(1,int(total_page) +1):
            url = f"{raw_url}?Page={i}"
            store_dict['normal_fetch'].append(url)
        
        normal_format_data(response_text, "normal_fetch", raw_result)
    elif fetch_status == "special_fetch_group_A":
        pass
