import pandas as pd
import json
from pathlib import Path
from app.config.paths import find_root_project

root = find_root_project()
json_config_name = "rawdata_config.json"

full_path = root / "app" / "config" / json_config_name

print(full_path)



def get_raw_data_configures(full_path:Path):
    try:
        if not full_path.exists():
            raise FileNotFoundError("Lỗi không tìm thấy file configure")
        with open(full_path, 'r', encoding='utf-8') as f:
            configure_data = json.load(f)
            return pd.DataFrame(configure_data)
    except Exception as e:
            print ("Có lỗi trong quá trình load file configure")