# datasources/endpoints/carros_modelos.py

from src.api_utils.api_connection import BaseConnector
import pandas as pd
import time

class RequestCarrosPorModelos(BaseConnector):
    def __init__(self, url):
        super().__init__(url)
    
    @BaseConnector.request_post()
    def get_table(self, response, *args, **kwargs):
        print("Tabela de Modelos: Dados recebidos com sucesso.")
        return response
    
    def get_carros_por_modelos(self, max_retries=3):
        df_marcas = pd.read_json('storage/raw/carros_marcas.json')
        resultados_modelos = []

        for codigo_marca in df_marcas['Value']:
            payload = {
                "codigoTabelaReferencia": 312,
                "codigoTipoVeiculo": 1,
                "codigoMarca": codigo_marca,
            }
            retries = 0
            while retries < max_retries:
                try:
                    response = self.get_table(data=payload)
                    if isinstance(response, dict) and 'Modelos' in response:
                        modelos_data = response['Modelos']
                        for modelo in modelos_data:
                            modelo['codigoMarca'] = codigo_marca
                            resultados_modelos.append(modelo)
                        break
                    else:
                        print(f"Resposta inválida para o codigoMarca {codigo_marca}: {response}")
                        break
                except Exception as e:
                    retries += 1
                    print(f"Erro ao obter dados para a marca {codigo_marca}: {e}. Tentativa {retries} de {max_retries}.")
                    time.sleep(1.5 + retries * 2)
            time.sleep(1.5 + retries * 1)

        return resultados_modelos
