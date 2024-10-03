# /dags/src/interfaces/base_extractor_interface.py
# Classe base abstrata para os extratores, implementando o padrão Template Method.

from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Generic
import logging

from src.api_utils.api_extractor_tools import ExtractorTools
from src.api_utils.api_connection import BaseConnector

TRequestClass = TypeVar('TRequestClass', bound=BaseConnector)

class BaseExtractorInterface(ABC, Generic[TRequestClass]):
    def __init__(self, url: str, request_class: Type[TRequestClass]) -> None:
        self._connector: TRequestClass = request_class(url)
        self._extractor_tools = ExtractorTools()

    @property
    def connector(self) -> TRequestClass:
        return self._connector

    @property
    def extractor_tools(self) -> ExtractorTools:
        return self._extractor_tools

    @abstractmethod
    def get_endpoint_data(self) -> None:
        pass

    @abstractmethod
    def saving_endpoint_data(self) -> None:
        pass

    def main(self) -> None:
        """
        Método Template que executa o fluxo de extração de dados e salvamento.
        """
        logging.info(f"Executando extração de dados com {self.__class__.__name__}")
        self.get_endpoint_data()
        self.saving_endpoint_data()
        logging.info(f"Dados extraídos e salvos com sucesso usando {self.__class__.__name__}.")
