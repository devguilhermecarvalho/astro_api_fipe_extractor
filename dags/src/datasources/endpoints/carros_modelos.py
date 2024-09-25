# src/datasources/endpoints/carros_modelos.py
# Classe para obter os modelos de carros a partir das marcas.

from src.api_utils.api_connection import BaseConnector
import pandas as pd
import time
import logging
from src.api_utils.api_config import CODIGO_TABELA_REFERENCIA

class RequestCarrosPorModelos(BaseConnector):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)

    def get_carros_por_modelos(self):
        df_marcas = pd.read_json('data/raw/carros_marcas.json')
        resultados_modelos = []

        for codigo_marca in df_marcas['Value']:
            payload = {
                "codigoTabelaReferencia": CODIGO_TABELA_REFERENCIA,
                "codigoTipoVeiculo": 1,
                "codigoMarca": codigo_marca,
            }
            response = self.post(data=payload)
            if response and 'Modelos' in response:
                modelos_data = response['Modelos']
                for modelo in modelos_data:
                    modelo['codigoMarca'] = codigo_marca
                    resultados_modelos.append(modelo)
                logging.info(f"Modelos obtidos para a marca {codigo_marca}.")
            else:
                logging.error(f"Resposta inválida para codigoMarca {codigo_marca}: {response}")
            time.sleep(self.delay)
        return resultados_modelos
