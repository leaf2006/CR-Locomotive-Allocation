import orjson
import asyncio
import re
from utils import utils
# from details_fetch import web_fetch

def normal_format_data(response_text :str,fetch_status :str, raw_result :list, detail_fetch_urls :list):
    """初步获取页面的主页信息，不包括制造商与设计时速，存入dict中"""
    if fetch_status == "normal_fetch":
        normal_page_match = re.findall(r'<a class="jytb" href="ProView\.asp\?ProId=(\d+)" target="_blank">([^<]+)</a>', response_text)
        normal_page_match = [(pid, text) for pid, text in normal_page_match if any('\u4e00' <= c <= '\u9fff' for c in text)]

        # detail_fetch_urls = []
        print(normal_page_match)
        for detail in normal_page_match:
            pro_id = detail[0]
            raw_train_detail = detail[1]
            raw_train_detail_split = raw_train_detail.split(' ') # 分割信息，只提取[1]：车型车号（全英文），[2]配属
            if len(raw_train_detail_split) < 3:
                train_series_number = raw_train_detail_split[1]
                train_allocation = "暂无配属"
            else:
                train_series_number = raw_train_detail_split[1]
                train_allocation = raw_train_detail_split[2] # 配属
            train_series = train_series_number.split('-')[0] # 型号
            url = f"http://www.xiaguanzhan.com/ProView.asp?ProId={pro_id}" # 详细页面url
            detail_fetch_urls.append(url)

            raw_result.setdefault(train_series, []).append({
                "id": train_series_number,
                "allocation": train_allocation,
                "manufacturer": "",
                "design_speed": ""
            })
            print(f"{train_series_number}已录入，配属：{train_allocation}")
