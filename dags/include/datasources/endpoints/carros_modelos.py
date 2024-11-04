from include.api_utils.api_connection import BaseConnector
import pandas as pd
import time
from include.api_utils.api_config import CODIGO_TABELA_REFERENCIA

class RequestCarrosPorModelos(BaseConnector):
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
            time.sleep(self.delay)
        return resultados_modelos
