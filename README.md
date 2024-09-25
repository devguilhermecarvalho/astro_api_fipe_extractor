# Projeto de Extração de Dados da API FIPE

Este projeto tem como objetivo extrair dados da API FIPE, processar e salvar as informações para uso posterior.

## Funcionalidades

- Extração de tabelas de referência, marcas, modelos e anos dos veículos.
- Processamento dos dados extraídos e salvamento em formatos JSON e CSV.
- Implementação de estrutura de logs para monitoramento do processo.
- Tratamento detalhado de erros durante as requisições à API.
- Uso do padrão de projeto Template Method para organização do código.

## Estrutura do Projeto

- `main.py`: Arquivo principal para execução dos extratores.
- `src/api_utils/`: Utilitários para conexão com a API e manipulação de dados.
- `src/datasources/endpoints/`: Classes específicas para cada endpoint da API.
- `src/interfaces/`: Interface base para os extratores.
- `data/raw/`: Pasta onde os dados extraídos são salvos.
- `logs/`: Pasta onde os logs diários são armazenados.

## Como Executar

1. Certifique-se de ter o Python 3.6 ou superior instalado.
2. Instale as dependências com o comando:
