from src.api_utils.api_config import API_INFO
from src.api_utils.api_extractor_tools import ExtractorTools

from src.database_tools.db_create_api_table import DatabaseTools

from src.api_endpoints.tabela_fipe_de_referencia import RequestFipeTabelaReferencia

# Dentro do datasources/endpoints
class ExtractorTabelaDeReferencia(BaseExtractor):
    def get_endpoint_data(self):
        self._tabela_de_referencia = self.connector.get_tabela_de_referencia()

    def saving_endpoint_data(self):
        self.extractor_tools.save_to_json(
            self._tabela_de_referencia, API_INFO['fipe_tabela_referencia']['save_path']
        )