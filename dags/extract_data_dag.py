# /dags/extract_data_dag.py
# DAG principal para extração de dados usando Airflow com decoradores.

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import sys
import os
from typing import Any

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datasources.endpoints.extractors import (
    ExtractorFipeTabelaReferencia,
    ExtractorCarrosMarcas,
    ExtractorCarrosPorModelos,
    ExtractorCarrosModelosPorAno,
    ExtractorTabelaFipeResultado
)

from api_utils.api_config import API_INFO
from datasources.endpoints.tabela_fipe_de_referencia import RequestFipeTabelaReferencia
from datasources.endpoints.carros_marcas import RequestCarrosMarcas
from datasources.endpoints.carros_modelos import RequestCarrosPorModelos
from datasources.endpoints.carros_modelos_por_ano import RequestModelosPorAno
from datasources.endpoints.tabela_fipe_resultado import RequestFipeResultado

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['seu_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    description='DAG para extrair dados da API FIPE',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['FIPE', 'data extraction'],
)
def extract_data_dag() -> None:
    @task()
    def extract_tabela_referencia() -> None:
        extractor = ExtractorFipeTabelaReferencia(
            API_INFO['fipe_tabela_referencia']['url'],
            RequestFipeTabelaReferencia
        )
        extractor.main()

    @task()
    def extract_carros_marcas() -> None:
        extractor = ExtractorCarrosMarcas(
            API_INFO['carros_marcas']['url'],
            RequestCarrosMarcas
        )
        extractor.main()

    @task()
    def extract_carros_modelos() -> None:
        extractor = ExtractorCarrosPorModelos(
            API_INFO['carros_modelos']['url'],
            RequestCarrosPorModelos
        )
        extractor.main()

    @task()
    def extract_carros_modelos_por_ano() -> None:
        extractor = ExtractorCarrosModelosPorAno(
            API_INFO['carros_ano_modelo']['url'],
            RequestModelosPorAno
        )
        extractor.main()

    @task()
    def extract_tabela_fipe_resultado() -> None:
        extractor = ExtractorTabelaFipeResultado(
            API_INFO['resultado_tabela_fipe']['url'],
            RequestFipeResultado
        )
        extractor.main()

    # Definição das dependências entre as tarefas
    extract_tabela_referencia_task = extract_tabela_referencia()
    extract_carros_marcas_task = extract_carros_marcas()
    extract_carros_modelos_task = extract_carros_modelos()
    extract_carros_modelos_por_ano_task = extract_carros_modelos_por_ano()
    extract_tabela_fipe_resultado_task = extract_tabela_fipe_resultado()

    extract_tabela_referencia_task >> extract_carros_marcas_task >> extract_carros_modelos_task >> extract_carros_modelos_por_ano_task >> extract_tabela_fipe_resultado_task

dag = extract_data_dag()