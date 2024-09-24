# main.py

from src.api_utils.api_config import API_INFO
from src.datasources.endpoints.tabela_fipe_de_referencia import RequestFipeTabelaReferencia
from src.datasources.endpoints.carros_marcas import RequestCarrosMarcas
from src.datasources.endpoints.carros_modelos import RequestCarrosPorModelos
from src.datasources.endpoints.carros_modelos_por_ano import RequestModelosPorAno
from src.datasources.endpoints.tabela_fipe_resultado import RequestFipeResultado

from src.datasources.endpoints.extractors import (
    ExtractorCarrosMarcas,
    ExtractorCarrosPorModelos,
    ExtractorCarrosModelosPorAno,
    ExtractorTabelaFipeResultado
)

extractors = [
    ExtractorCarrosMarcas(API_INFO['carros_marcas']['url'], RequestCarrosMarcas),
    ExtractorCarrosPorModelos(API_INFO['carros_modelos']['url'], RequestCarrosPorModelos),
    ExtractorCarrosModelosPorAno(API_INFO['carros_ano_modelo']['url'], RequestModelosPorAno),
    ExtractorTabelaFipeResultado(API_INFO['resultado_tabela_fipe']['url'], RequestFipeResultado)
]

for extractor in extractors:
    extractor.main()