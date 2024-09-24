# src/interfaces/base_extractor_interface.py
from abc import ABC, abstractmethod
from src.api_utils.api_extractor_tools import ExtractorTools

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
        self.get_endpoint_data()
        self.saving_endpoint_data()
