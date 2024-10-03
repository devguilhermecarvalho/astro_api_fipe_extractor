# /dags/src/datasources/endpoints/tabela_referencia.py
# Classe para obter a tabela de referência FIPE.

from src.api_utils.api_connection import BaseConnector
import logging
from typing import Optional, Dict, Any

class RequestFipeTabelaReferencia(BaseConnector):
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None) -> None:
        super().__init__(url, headers)

    def get_tabela_de_referencia(self) -> Optional[List[Dict[str, Any]]]:
        payload: Dict[str, Any] = {}
        response = self.post(data=payload)
        if response:
            logging.info("Tabela de Referência: Dados recebidos com sucesso.")
            return response
        else:
            logging.error("Falha ao obter a tabela de referência.")
            return None