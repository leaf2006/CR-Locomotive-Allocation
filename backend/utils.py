from pathlib import Path
import orjson
import re

# def result_data_initialization():
#     current_dir = Path(__file__).parent
#     data_dir = current_dir.parent / "data"
#     raw_result_path = data_dir / "raw_result.json"

class utils:
    def fetch_divide(raw_data :list, store :list) -> list:
        """将所有数据分为十个一组"""
        for i in range(0, len(raw_data), 10):
            batch = raw_data[i:i+10]
            store.append(batch)
    def xiaguanzhan_first_match(pattern, text):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else None