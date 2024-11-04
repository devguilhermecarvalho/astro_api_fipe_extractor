from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from include.datasources.endpoints.extractors import (
    ExtractorFipeTabelaReferencia,
    ExtractorCarrosMarcas,
    ExtractorCarrosPorModelos,
    ExtractorCarrosModelosPorAno,
    ExtractorTabelaFipeResultado,
)

from include.api_utils.api_config import API_INFO
from include.datasources.endpoints.tabela_fipe_de_referencia import RequestFipeTabelaReferencia
from include.datasources.endpoints.carros_marcas import RequestCarrosMarcas
from include.datasources.endpoints.carros_modelos import RequestCarrosPorModelos
from include.datasources.endpoints.carros_modelos_por_ano import RequestModelosPorAno
from include.datasources.endpoints.tabela_fipe_resultado import RequestFipeResultado

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['seu_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'extract_data_dag',
    default_args=default_args,
    description='DAG para extrair dados da API FIPE',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 10, 1),
    catchup=False,
)

def extract_tabela_referencia(**context):
    extractor = ExtractorFipeTabelaReferencia(
        API_INFO['fipe_tabela_referencia']['url'], RequestFipeTabelaReferencia
    )
    extractor.main()

def extract_carros_marcas(**context):
    extractor = ExtractorCarrosMarcas(
        API_INFO['carros_marcas']['url'], RequestCarrosMarcas
    )
    extractor.main()

def extract_carros_modelos(**context):
    extractor = ExtractorCarrosPorModelos(
        API_INFO['carros_modelos']['url'], RequestCarrosPorModelos
    )
    extractor.main()

def extract_carros_modelos_por_ano(**context):
    extractor = ExtractorCarrosModelosPorAno(
        API_INFO['carros_ano_modelo']['url'], RequestModelosPorAno
    )
    extractor.main()

def extract_tabela_fipe_resultado(**context):
    extractor = ExtractorTabelaFipeResultado(
        API_INFO['resultado_tabela_fipe']['url'], RequestFipeResultado
    )
    extractor.main()

task_extract_tabela_referencia = PythonOperator(
    task_id='extract_tabela_referencia',
    python_callable=extract_tabela_referencia,
    dag=dag,
)

task_extract_carros_marcas = PythonOperator(
    task_id='extract_carros_marcas',
    python_callable=extract_carros_marcas,
    dag=dag,
)

task_extract_carros_modelos = PythonOperator(
    task_id='extract_carros_modelos',
    python_callable=extract_carros_modelos,
    dag=dag,
)

task_extract_carros_modelos_por_ano = PythonOperator(
    task_id='extract_carros_modelos_por_ano',
    python_callable=extract_carros_modelos_por_ano,
    dag=dag,
)

task_extract_tabela_fipe_resultado = PythonOperator(
    task_id='extract_tabela_fipe_resultado',
    python_callable=extract_tabela_fipe_resultado,
    dag=dag,
)

task_extract_tabela_referencia >> task_extract_carros_marcas >> task_extract_carros_modelos >> task_extract_carros_modelos_por_ano >> task_extract_tabela_fipe_resultado