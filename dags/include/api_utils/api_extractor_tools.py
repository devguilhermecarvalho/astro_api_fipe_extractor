import json
import os
import pandas as pd

class ExtractorTools:
    def save_to_csv(self, data, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    def save_to_json(self, data, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
