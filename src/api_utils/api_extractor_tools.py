# src/api_utils/api_extractor_tools.py

import json
from typing import List, Dict, Any
import os

import pandas as pd

class ExtractorTools:
    def extract(self, data: List[Dict[str,Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return df
    
    def extract_inlist(self, data):
        df = pd.DataFrame([data])
        return df

    def save_to_csv(self, data, file_path: str):
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"Dados salvos em {file_path}")

    def save_to_parquet(self, data, file_path: str):
        df = pd.DataFrame(data)
        df.to_parquet(file_path, index=False)
        print(f"Dados salvos em {file_path}")
    
    def save_to_json(self, data, file_path: str):
        # Certifique-se de que o diretório existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Salvar o JSON com codificação UTF-8
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Dados salvos em {file_path}")