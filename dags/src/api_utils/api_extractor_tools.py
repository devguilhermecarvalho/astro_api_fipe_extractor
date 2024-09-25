# src/api_utils/api_extractor_tools.py
# Ferramentas para extração e salvamento de dados.

import json
import os
import pandas as pd
import logging

class ExtractorTools:
    def extract(self, data):
        return pd.DataFrame(data)

    def save_to_csv(self, data, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        logging.info(f"Dados salvos em {file_path}")

    def save_to_json(self, data, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        logging.info(f"Dados salvos em {file_path}")
