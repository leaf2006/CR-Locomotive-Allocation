# import sys
import re

# sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def format_data(response_text: str, item: dict, result: list):  # FIX: 参数从 (train_info, raw_result) 改为 (item, result)
    """提取response_text中的有用信息，更新item并整合进result dict中"""

    train_series = item['train_series']  # FIX: 从 item 直接取车型，取代原来的 train_info[0]

    locomotive_match = re.search(r'<td height="11" class="content"><P><FONT face=Verdana>([\s\S]*)</FONT></P></td>', response_text)
    emu_match = re.search(r'<td height="11" class="content"><p><P><FONT face=Verdana>([\s\S]*?)</FONT></P></p>', response_text)

    try:
        if locomotive_match:
            raw_data_group = locomotive_match.group(1)
            manufacturer = re.search(r'生产厂商：(.*?)<BR>', raw_data_group).group(1)
            design_speed = re.search(r'运行时速：(.*?)(?:<BR>|</FONT>)', raw_data_group).group(1)
            photo_date = re.search(r'拍摄日期：(.*?)<BR>', raw_data_group).group(1)
            photo_author = re.search(r'拍摄作者：(.+)', raw_data_group).group(1)

        elif emu_match:
            raw_data_group = emu_match.group(1)
            design_speed = re.search(r'运行时速：(.*?)</FONT>', raw_data_group).group(1)
            manufacturer = re.search(r'生产厂商：(.*?)<BR>', raw_data_group).group(1)
            photo_date = re.search(r'拍摄日期：(.*?)<BR>', raw_data_group).group(1)
            photo_author = re.search(r'拍摄作者：(.+)', raw_data_group).group(1)

        # else:
        #     print(f"[ERROR] locomotive_match和emu_match均未匹配，id: {item['id']}")
        #     print(f"[ERROR] response_text: {response_text}")
        #     return

        photo_url = re.search(r'<td width="652"><a href="(.*?)"></a>', response_text).group(1)

        # FIX: 直接更新传入的 item，取代原来按 train_series + id 查找的循环
        item["manufacturer"] = manufacturer
        item["photo_url"] = f"http://www.xiaguanzhan.com/{photo_url}"
        item["photo_date"] = photo_date
        item["photo_author"] = photo_author

        # FIX: 以 train_series 为 key 将 item 整合进 result dict
        # if train_series not in result:
        #     result[train_series] = []
        # result[train_series].append(item)
        result.append(item)

        print(f"已录入{item['id']}，生产厂商：{manufacturer}，图片链接：{photo_url}，拍摄日期：{photo_date}，拍摄作者：{photo_author}")
    except Exception as e:
        pass
        # print(f"[ERROR] 处理{item['id']}时出错: {e}")
        # print(f"[ERROR] response_text: {response_text}")