import orjson
import asyncio
import re
from bs4 import BeautifulSoup
from utils import utils
# from details_fetch import web_fetch

def format_data(response_text :str,fetch_status :str, raw_result :list):
    """初步获取页面的主页信息，不包括制造商与设计时速，存入dict中"""
    status = "normal_xiaguan"
    if fetch_status == "normal_fetch":
        normal_page_match = re.findall(r'<a class="jytb" href="ProView\.asp\?ProId=(\d+)" target="_blank">([^<]+)</a>', response_text)
        page_match = [(pid, text) for pid, text in normal_page_match if any('\u4e00' <= c <= '\u9fff' for c in text)]
    elif fetch_status == "special_fetch":
        special_page_match = re.findall(r'<td height="33"><div align="center"><span class="bottombr"><a href="ProView\.asp\?ProId=(\d+)" target="_blank">([^<]+)</a></span></div></td>', response_text)
        page_match = [(pid, text) for pid, text in special_page_match if any('\u4e00' <= c <= '\u9fff' for c in text)]
    elif fetch_status == "emu_normal_fetch":
        status = "emu"
        soup = BeautifulSoup(response_text, "html.parser") # 使用beautifulsoup便于分析
        emu_entries = []
        detail_link_re = re.compile(r"emu_detail\.php\?keyword=")
        keyword_re = re.compile(r"keyword=\s*([^&\s]+)")

        for link in soup.find_all("a", href=detail_link_re):
            href = link.get("href", "")
            match = keyword_re.search(href)
            if not match:
                continue
            keyword = match.group(1)
            row = link.find_parent("tr")
            if not row:
                continue

            cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
            if len(cells) < 6:
                continue

            bureau = cells[2] # 配属路局
            department = cells[3] # 所属动车所
            manufacturer = cells[4] # 生产厂家
            note = cells[5] 

            emu_entries.append({
                "keyword": keyword,
                "bureau": bureau,
                "department": department,
                "manufacturer": manufacturer,
                "note": note,
            })
    elif fetch_status == "emu_normal_fetch_xiaguan":
        status = "emu_xiaguan"
        special_page_match = re.findall(r'<td height="\d+"><div align="center"><span class="bottombr"><a href="ProView\d*\.asp\?ProId=(\d+)" target="_blank">([^<]+)</a></span></div></td>', response_text)
        page_match = [(pid, text) for pid, text in special_page_match if any('\u4e00' <= c <= '\u9fff' for c in text)]        

    # print(page_match)
    if status == "normal_xiaguan":
        for detail in page_match:
            pro_id = detail[0]
            raw_train_detail = detail[1]
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
                "pro_id": pro_id
                # "manufacturer": "",
                # "design_speed": ""
            })
            print(f"[INFO] {train_series_number}已录入，配属：{train_allocation} PRO ID：{pro_id}")
    elif status == "emu":
        for entry in emu_entries:
            train_series = entry["keyword"].rsplit('-', 1)[0]
            if entry['bureau'] == "" and entry['department'] == "":
                allocation = "暂无数据"
            else:
                allocation = f"{entry['bureau']}{entry['department']}动车所"
            raw_result.setdefault(train_series, []).append({
                "id": entry["keyword"],
                "allocation": allocation,
                "manufacturer": entry["manufacturer"],
                "note": entry["note"],
                "pro_id": ""
            })
            print(f"[INFO] {entry["keyword"]}已录入，配属：{allocation}")
    elif status == "emu_xiaguan": # 这里的raw_result使用的是emu_xiaguan_result
        for detail in page_match:
            pro_id = detail[0]
            raw_train_detail = detail[1]
            train_series_number = raw_train_detail.split(' ')[0]
            train_series = train_series_number.split('-')[0]

            raw_result.setdefault(train_series, []).append({
                "id": train_series_number,
                "pro_id": pro_id
            })
            print(f"[INFO] {train_series_number}（下关站）已录入，PRO ID：{pro_id}，稍后将会与emu_normal_fetch进行比对")

def get_webfetch_data(response_text :str, fetch_status :str, raw_url :str, store_dict :list, raw_result :list):
    """获取当前组的信息总量、总页数，顺便获取当页的信息"""
    total_page_match = re.search(r"\[页次<Font color='Red'>1</Font>/(.*?)页\]", response_text)
    emu_page_match = re.search(r"\(1/(\d{1,2})\)", response_text)

    if total_page_match:
        total_page = total_page_match.group(1)
    elif emu_page_match:
        total_page = emu_page_match.group(1)
    else:
        total_page = "1" # 这种情况下，当前页面只有第一页
        

    if fetch_status == "normal_fetch":
        for i in range(2,int(total_page) +1):
            url = f"{raw_url}?Page={i}"
            store_dict['normal_fetch'].append(url)
        format_data(response_text, "normal_fetch", raw_result)

    elif fetch_status == "special_fetch":
        for i in range(2,int(total_page) +1):
            url = f"{raw_url}&Page={i}"
            store_dict['special_fetch'].append(url)  
        format_data(response_text, "special_fetch", raw_result)   

    elif fetch_status == "emu_normal_fetch":
        for i in range(2,int(total_page) +1):
            url = f"{raw_url}&pagenum={i}"
            store_dict['emu_normal_fetch'].append(url)
        format_data(response_text, "emu_normal_fetch", raw_result)
    
    elif fetch_status == "emu_normal_fetch_xiaguan":
        # 这里的车型数据使用?Page=来进行翻页
        models_without_query_params = ['CRH2A','CRH2B','CRH5A','CRH6F-A','CRH380B','CR300BF'] 
        for i in range(2,int(total_page) +1):
            use_question = any(m in raw_url for m in models_without_query_params)
            url = f"{raw_url}?Page={i}" if use_question else f"{raw_url}&Page={i}"
            store_dict['emu_normal_fetch_xiaguan'].append(url)
        format_data(response_text, "emu_normal_fetch_xiaguan", raw_result) # 这里的raw_result是emu_xiaguan_compare
