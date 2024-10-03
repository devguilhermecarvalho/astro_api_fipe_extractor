# main.py
# Arquivo principal para executar os extratores.

from dags.src.api_utils.api_config import API_INFO
from dags.src.datasources.endpoints.carros_marcas import RequestCarrosMarcas
from dags.src.datasources.endpoints.carros_modelos import RequestCarrosPorModelos
from dags.src.datasources.endpoints.carros_modelos_por_ano import RequestModelosPorAno
from dags.src.datasources.endpoints.tabela_fipe_resultado import RequestFipeResultado
from dags.src.datasources.endpoints.tabela_fipe_de_referencia import RequestFipeTabelaReferencia

from dags.src.datasources.endpoints.extractors import (
    ExtractorCarrosMarcas,
    ExtractorCarrosPorModelos,
    ExtractorCarrosModelosPorAno,
    ExtractorTabelaFipeResultado,
    ExtractorFipeTabelaReferencia
)

def main() -> None:
    extractors = [
        ExtractorFipeTabelaReferencia(API_INFO['fipe_tabela_referencia']['url'], RequestFipeTabelaReferencia),
        ExtractorCarrosMarcas(API_INFO['carros_marcas']['url'], RequestCarrosMarcas),
        ExtractorCarrosPorModelos(API_INFO['carros_modelos']['url'], RequestCarrosPorModelos),
        ExtractorCarrosModelosPorAno(API_INFO['carros_ano_modelo']['url'], RequestModelosPorAno),
        ExtractorTabelaFipeResultado(API_INFO['resultado_tabela_fipe']['url'], RequestFipeResultado)
    ]

    for extractor in extractors:
        extractor.main()

if __name__ == "__main__":
    main()