import orjson
import asyncio
import re

def get_webfetch_data(response_text :str, is_normal_fetch :bool, raw_url :str, store_dict :list):
    """获取当前组的信息总量、总页数，顺便获取当页的信息"""
    if is_normal_fetch == True:
        # total_match = re.search(r"共<Font color='Red'><b>(.*?)</b></Font>条记录", response_text)
        # if total_match:
        #     total = total_match.group(1)
        total_page_match = re.search(r"\[页次<Font color='Red'>1</Font>/(.*?)页\]", response_text)
        if total_page_match:
            total_page = total_page_match.group(1)

        for i in range(1,int(total_page) +1):
            url = f"{raw_url}?Page={i}"
            store_dict.append(url)