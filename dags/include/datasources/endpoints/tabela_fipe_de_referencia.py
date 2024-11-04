from include.api_utils.api_connection import BaseConnector

class RequestFipeTabelaReferencia(BaseConnector):
    def get_tabela_de_referencia(self):
        payload = {}
        response = self.post(data=payload)
        return response