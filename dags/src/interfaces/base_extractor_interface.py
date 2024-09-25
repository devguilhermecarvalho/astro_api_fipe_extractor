# src/interfaces/base_extractor_interface.py
# Classe base abstrata para os extratores, implementando o padrão Template Method.

from abc import ABC, abstractmethod
from src.api_utils.api_extractor_tools import ExtractorTools
import logging

class BaseExtractorInterface(ABC):
    def __init__(self, url, request_class):
        self._connector = request_class(url)
        self._extractor_tools = ExtractorTools()

    @property
    def connector(self):
        return self._connector

    @property
    def extractor_tools(self):
        return self._extractor_tools

    @abstractmethod
    def get_endpoint_data(self):
        pass

    @abstractmethod
    def saving_endpoint_data(self):
        pass

    def main(self):
        """
        Método Template que executa o fluxo de extração de dados e salvamento.
        """
        logging.info(f"Executando extração de dados com {self.__class__.__name__}")
        self.get_endpoint_data()
        self.saving_endpoint_data()
        logging.info(f"Dados extraídos e salvos com sucesso usando {self.__class__.__name__}.")
