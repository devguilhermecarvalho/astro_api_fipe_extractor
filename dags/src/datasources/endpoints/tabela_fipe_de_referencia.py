# src/datasources/endpoints/tabela_fipe_de_referencia.py
# Classe para obter a tabela de referência FIPE.

from src.api_utils.api_connection import BaseConnector
import logging

class RequestFipeTabelaReferencia(BaseConnector):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)

    def get_tabela_de_referencia(self):
        payload = {}
        response = self.post(data=payload)
        if response:
            logging.info("Tabela de Referência: Dados recebidos com sucesso.")
            return response
        else:
            logging.error("Falha ao obter a tabela de referência.")
            return None
