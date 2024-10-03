# /dags/src/api_utils/api_connection.py
# BaseConnector: responsável por realizar as conexões com a API, lidando com tentativas e tratamento de erros.

import requests
import time
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Configuração do logger para salvar logs em arquivos diários
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, datetime.now().strftime('%Y-%m-%d') + '.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='w'),
        logging.StreamHandler()
    ]
)

class BaseConnector:
    def __init__(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
        delay: float = 1.5
    ) -> None:
        self.url = url
        self.headers = headers or {}
        self.max_retries = max_retries
        self.delay = delay

    def post(self, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(self.url, json=data, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    logging.error(f"Erro na requisição: {response.status_code} - {response.text}")
                    return None
            except requests.exceptions.Timeout:
                logging.error("A requisição excedeu o tempo limite.")
            except requests.exceptions.ConnectionError:
                logging.error("Erro de conexão com a API.")
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro inesperado na requisição: {e}")
            retries += 1
            logging.info(f"Tentativa {retries} de {self.max_retries}. Aguardando {self.delay * retries} segundos.")
            time.sleep(self.delay * retries)
        return None