# datasources/endpoints/extractors.py

from src.interfaces.base_extractor_interface import BaseExtractorInterface
from src.api_utils.api_config import API_INFO
from src.database_tools.db_create_api_table import DatabaseTools

class ExtractorCarrosMarcas(BaseExtractorInterface):
    def get_endpoint_data(self):
        self._tabela_de_carros_marcas = self.connector.get_tabela_de_carros_marcas()

    def saving_endpoint_data(self):
        self.extractor_tools.save_to_json(
            self._tabela_de_carros_marcas, API_INFO['carros_marcas']['save_path']
        )
        db_tools = DatabaseTools()
        db_tools.create_table("carros_marcas", self._tabela_de_carros_marcas)
        db_tools.close_connection()


class ExtractorCarrosPorModelos(BaseExtractorInterface):
    def get_endpoint_data(self):
        self._tabela_de_carros_por_modelos = self.connector.get_carros_por_modelos()

    def saving_endpoint_data(self):
        self.extractor_tools.save_to_json(
            self._tabela_de_carros_por_modelos, API_INFO['carros_modelos']['save_path']
        )


class ExtractorCarrosModelosPorAno(BaseExtractorInterface):
    def get_endpoint_data(self):
        self._tabela_de_carros_modelos_por_ano = self.connector.get_tabela_carros_modelos_por_ano()

    def saving_endpoint_data(self):
        self.extractor_tools.save_to_json(
            self._tabela_de_carros_modelos_por_ano, API_INFO['carros_ano_modelo']['save_path']
        )


class ExtractorTabelaFipeResultado(BaseExtractorInterface):
    def get_endpoint_data(self):
        self._tabela_fipe_resultado = self.connector.get_tabela_de_resultado_fipe()

    def saving_endpoint_data(self):
        self.extractor_tools.save_to_csv(
            self._tabela_fipe_resultado, API_INFO['resultado_tabela_fipe']['save_path']
        )