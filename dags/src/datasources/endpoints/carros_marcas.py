# src/datasources/endpoints/carros_marcas.py
# Classe para realizar requisições e obter a tabela de marcas de carros.

from src.api_utils.api_connection import BaseConnector
import logging
from src.api_utils.api_config import CODIGO_TABELA_REFERENCIA

class RequestCarrosMarcas(BaseConnector):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)

    def get_tabela_de_carros_marcas(self):
        payload = {
            "codigoTabelaReferencia": CODIGO_TABELA_REFERENCIA,
            "codigoTipoVeiculo": 1
        }
        response = self.post(data=payload)
        if response is not None:
            logging.info("Tabela de Marcas: Dados recebidos com sucesso.")
            return response
        else:
            logging.error("Falha ao obter a tabela de marcas.")
            return None