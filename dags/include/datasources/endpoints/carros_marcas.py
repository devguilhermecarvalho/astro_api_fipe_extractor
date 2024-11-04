from include.api_utils.api_connection import BaseConnector
from include.api_utils.api_config import CODIGO_TABELA_REFERENCIA

class RequestCarrosMarcas(BaseConnector):
    def get_tabela_de_carros_marcas(self):
        payload = {
            "codigoTabelaReferencia": CODIGO_TABELA_REFERENCIA,
            "codigoTipoVeiculo": 1
        }
        response = self.post(data=payload)
        return response
