# datasources/endpoints/carros_marcas.py

from src.api_utils.api_connection import BaseConnector

class RequestCarrosMarcas(BaseConnector):
    def __init__(self, url):
        super().__init__(url)

    @BaseConnector.request_post()
    def get_table(self, response, *args, **kwargs):
        print("Tabela de Marcas: Dados recebidos com sucesso.")
        return response

    def get_tabela_de_carros_marcas(self):
        payload = {
            "codigoTabelaReferencia": 312,
            "codigoTipoVeiculo": 1
        }
        return self.get_table(data=payload)
