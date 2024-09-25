# src/datasources/endpoints/extractors.py
# Implementação dos extratores específicos, seguindo o padrão Template Method.

from src.interfaces.base_extractor_interface import BaseExtractorInterface
from src.api_utils.api_config import API_INFO
import logging

class ExtractorCarrosMarcas(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.data = self.connector.get_tabela_de_carros_marcas()

    def saving_endpoint_data(self):
        if self.data:
            self.extractor_tools.save_to_json(
                self.data, API_INFO['carros_marcas']['save_path']
            )
        else:
            logging.error("Erro: Nenhum dado foi recebido.")

class ExtractorCarrosPorModelos(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.data = self.connector.get_carros_por_modelos()

    def saving_endpoint_data(self):
        if self.data:
            self.extractor_tools.save_to_json(
                self.data, API_INFO['carros_modelos']['save_path']
            )
        else:
            logging.error("Erro: Nenhum dado foi recebido.")

class ExtractorCarrosModelosPorAno(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.connector.get_tabela_carros_modelos_por_ano()

    def saving_endpoint_data(self):
        # Os dados são salvos diretamente no método do conector.
        pass

class ExtractorTabelaFipeResultado(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.connector.get_tabela_de_resultado_fipe()

    def saving_endpoint_data(self):
        # Os dados são salvos diretamente no método do conector.
        pass

class ExtractorFipeTabelaReferencia(BaseExtractorInterface):
    def get_endpoint_data(self):
        self.data = self.connector.get_tabela_de_referencia()

    def saving_endpoint_data(self):
        if self.data:
            self.extractor_tools.save_to_json(
                self.data, API_INFO['fipe_tabela_referencia']['save_path']
            )
        else:
            logging.error("Erro: Nenhum dado foi recebido.")
