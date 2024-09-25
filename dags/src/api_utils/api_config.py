# src/api_utils/api_config.py
# Configurações da API FIPE, incluindo URLs, cabeçalhos e caminhos para salvar os dados.


BASE_URL = "https://veiculos.fipe.org.br/api/veiculos"
BASE_STORAGE_PATH = "data/raw"
COMMON_HEADERS = {"Content-Type": "application/json"}

CODIGO_TABELA_REFERENCIA = 312

API_INFO = {
    "fipe_tabela_referencia": {
        "url": f"{BASE_URL}/ConsultarTabelaDeReferencia",
        "save_path": f"{BASE_STORAGE_PATH}/fipe_tabela_referencia.json",
        "headers": COMMON_HEADERS
    },
    "carros_marcas": {
        "url": f"{BASE_URL}/ConsultarMarcas",
        "save_path": f"{BASE_STORAGE_PATH}/carros_marcas.json",
        "headers": COMMON_HEADERS
    },
    "carros_modelos": {
        "url": f"{BASE_URL}/ConsultarModelos",
        "save_path": f"{BASE_STORAGE_PATH}/carros_modelos.json",
        "headers": COMMON_HEADERS
    },
    "carros_tipos": {
        "url": f"{BASE_URL}/ConsultarTipoVeiculo",
        "save_path": f"{BASE_STORAGE_PATH}/carros_tipos.json",
        "headers": COMMON_HEADERS
    },
    "carros_ano_modelo": {
        "url": f"{BASE_URL}/ConsultarAnoModelo",
        "save_path": f"{BASE_STORAGE_PATH}/carros_ano_modelo.json",
        "headers": COMMON_HEADERS
    },
    "carros_modelos_atraves_do_ano": {
        "url": f"{BASE_URL}/ConsultarModelosAtravesDoAno",
        "save_path": f"{BASE_STORAGE_PATH}/carros_modelos_atraves_do_ano.json",
        "headers": COMMON_HEADERS
    },
    "resultado_tabela_fipe": {
        "url": f"{BASE_URL}/ConsultarValorComTodosParametros",
        "save_path": f"{BASE_STORAGE_PATH}/resultado_tabela_fipe.json",
        "headers": COMMON_HEADERS
    }
}