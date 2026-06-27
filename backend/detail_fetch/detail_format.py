# import sys
import re

# sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def format_data(response_text: str, item: dict, result: list):  # FIX: 参数从 (train_info, raw_result) 改为 (item, result)
    """提取response_text中的有用信息，更新item并整合进result dict中"""

    train_series = item['train_series']  # FIX: 从 item 直接取车型，取代原来的 train_info[0]

    # 各种HTML结构的正则模式：
    # match_1: <td class="content"><P><FONT face=Verdana>...  （含FONT包裹P的标准格式）
    match_1 = re.search(r'<td height="11" class="content"><P><FONT face=Verdana>([\s\S]*)</FONT>[\s\S]*?</td>', response_text)
    # match_2: <td class="content"><p><P><FONT face=Verdana>...  （双层P标签格式）
    match_2 = re.search(r'<td height="11" class="content"><p><P><FONT face=Verdana>([\s\S]*?)</FONT></P></p>', response_text)
    # match_3: <td class="content"><P>机车名称...  （无FONT包裹，直接P标签格式）
    match_3 = re.search(r'<td height="11" class="content">(<P>(?!<FONT)[\s\S]*?</td>)', response_text)
    # match_4: <td class="content"><FONT face=Verdana>\n<P><FONT face=Verdana>...  （外层FONT包裹整个td内容）
    match_4 = re.search(r'<td height="11" class="content"><FONT face=Verdana>[\r\n\s]*(<P>[\s\S]*?)</FONT></td>', response_text)
    # match_5: <td class="content">机车名称：...  （老式平铺格式，无P标签）
    match_5 = re.search(r'<td height="11" class="content">(机车名称：[\s\S]*?)</td>', response_text)

    try:
        if match_1:
            raw_data_group = match_1.group(1)
            manufacturer = re.search(r'生产厂商：(.*?)<BR>', raw_data_group)
            manufacturer = manufacturer.group(1) if manufacturer else "暂无数据"
            design_speed = re.search(r'运行时速：(.*?)(?:<BR>|</FONT>)', raw_data_group)
            design_speed = design_speed.group(1) if design_speed else "暂无数据"
            photo_date = re.search(r'拍摄日期：(.*?)<BR>', raw_data_group)
            photo_date = photo_date.group(1) if photo_date else "暂无数据"
            photo_author = re.search(r'拍摄作者：(.+)', raw_data_group)
            photo_author = photo_author.group(1) if photo_author else "暂无数据"

        elif match_2:
            raw_data_group = match_2.group(1)
            design_speed = re.search(r'运行时速：(.*?)</FONT>', raw_data_group)
            design_speed = design_speed.group(1) if design_speed else "暂无数据"
            manufacturer = re.search(r'生产厂商：(.*?)<BR>', raw_data_group)
            manufacturer = manufacturer.group(1) if manufacturer else "暂无数据"
            photo_date = re.search(r'拍摄日期：(.*?)<BR>', raw_data_group)
            photo_date = photo_date.group(1) if photo_date else "暂无数据"
            photo_author = re.search(r'拍摄作者：(.+)', raw_data_group)
            photo_author = photo_author.group(1) if photo_author else "暂无数据"

        elif match_3 or match_4:
            # 无FONT包裹P标签格式 / 外层FONT包裹整个td格式
            # 两者内部字段提取逻辑相同，均通过 <BR> 分隔
            raw_data_group = (match_3 or match_4).group(1)
            manufacturer = re.search(r'生产厂商：(.*?)<BR>', raw_data_group)
            manufacturer = manufacturer.group(1) if manufacturer else "暂无数据"
            design_speed = re.search(r'运行时速：(.*?)(?:<BR>|</FONT>|</P>)', raw_data_group)
            design_speed = design_speed.group(1) if design_speed else "暂无数据"
            photo_date = re.search(r'拍摄日期：(?:<FONT[^>]*>)?(.*?)(?:</FONT>)?<BR>', raw_data_group)
            photo_date = photo_date.group(1) if photo_date else "暂无数据"
            photo_author = re.search(r'拍摄作者：(?:<FONT[^>]*>)?([^<\r\n]+)', raw_data_group)
            photo_author = photo_author.group(1) if photo_author else "暂无数据"

        elif match_5:
            # 老式平铺格式（无P标签，字段直接换行用<BR>分隔）
            raw_data_group = match_5.group(1)
            manufacturer = re.search(r'生产厂商：(.*?)[\s]*<BR>', raw_data_group)
            manufacturer = manufacturer.group(1).strip() if manufacturer else "暂无数据"
            design_speed = re.search(r'运行时速：(.*?)[\s]*<BR>', raw_data_group)
            design_speed = design_speed.group(1).strip() if design_speed else "暂无数据"
            photo_date = re.search(r'拍摄日期：(?:<FONT[^>]*>)?(.*?)(?:</FONT>)?<BR>', raw_data_group)
            photo_date = photo_date.group(1).strip() if photo_date else "暂无数据"
            photo_author = re.search(r'拍摄作者：(?:<FONT[^>]*>)?([^<\r\n]+)', raw_data_group)
            photo_author = photo_author.group(1).strip() if photo_author else "暂无数据"

        else:
            manufacturer = "暂无数据"
            design_speed = "暂无数据"
            photo_date = "暂无数据"
            photo_author = "暂无数据"

        photo_url_match = re.search(r'<td width="652"><a href="(.*?)"></a>', response_text)
        photo_url = photo_url_match.group(1) if photo_url_match else "暂无数据"

        # FIX: 直接更新传入的 item，取代原来按 train_series + id 查找的循环
        item["manufacturer"] = manufacturer
        item["photo_url"] = f"http://www.xiaguanzhan.com/{photo_url}" if photo_url != "暂无数据" else "暂无数据"
        item["photo_date"] = photo_date
        item["photo_author"] = photo_author

        result.append(item)

        print(f"已录入{item['id']}，生产厂商：{manufacturer}，图片链接：{photo_url}，拍摄日期：{photo_date}，拍摄作者：{photo_author}")
    except Exception as e:
        print(f"[ERROR] {str(e)}")