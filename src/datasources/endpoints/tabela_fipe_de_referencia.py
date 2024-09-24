# datasources/endpoints/tabela_fipe_de_referencia.py

from src.api_utils.api_connection import BaseConnector

class RequestFipeTabelaReferencia(BaseConnector):
    def __init__(self, url):
        super().__init__(url)

    @BaseConnector.request_post()
    def get_table(self, response, *args, **kwargs):
        print("Tabela de Referência: Dados recebidos com sucesso.")
        return response

    def get_tabela_de_referencia(self):
        payload = {
            "codigoTabelaReferencia": 312,
            "codigoTipoVeiculo": 1
        }
        return self.get_table(data=payload)
