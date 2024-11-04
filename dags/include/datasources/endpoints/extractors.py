from include.interfaces.base_extractor_interface import BaseExtractorInterface
from include.api_utils.api_config import API_INFO

class ExtractorCarrosMarcas(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.data = self.connector.get_tabela_de_carros_marcas()

    def saving_endpoint_data(self):
        if self.data:
            self.extractor_tools.save_to_json(
                self.data, API_INFO['carros_marcas']['save_path']
            )

class ExtractorCarrosPorModelos(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.data = self.connector.get_carros_por_modelos()

    def saving_endpoint_data(self):
        if self.data:
            self.extractor_tools.save_to_json(
                self.data, API_INFO['carros_modelos']['save_path']
            )

class ExtractorCarrosModelosPorAno(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.connector.get_tabela_carros_modelos_por_ano()

    def saving_endpoint_data(self):
        pass

class ExtractorTabelaFipeResultado(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.connector.get_tabela_de_resultado_fipe()

    def saving_endpoint_data(self):
        pass

class ExtractorFipeTabelaReferencia(BaseExtractorInterface):

    def get_endpoint_data(self):
        self.data = self.connector.get_tabela_de_referencia()

    def saving_endpoint_data(self):
        if self.data:
            self.extractor_tools.save_to_json(
                self.data, API_INFO['fipe_tabela_referencia']['save_path']
            )
