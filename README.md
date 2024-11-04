# Projeto de Extração de Dados da API FIPE

Este projeto tem como objetivo extrair dados da API FIPE utilizando um ambiente Astronomer com Airflow para orquestração das tarefas que facilita o gerenciamento e implantação de fluxos de trabalho.

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

## Pré-requisitos

- Docker instalado.

## Como Executar no Ubuntu

- Verifique e instale o docker na sua máquina.

1. Faça a cópia do projeto:
   1. CMD: `git clone`
2. Faça o download e instalação do Astronomer:
   1. CMD: `curl -sSL https://install.astronomer.io | sudo bash`
3. Preparando o ambiente virtual na pasta do projeto:
   1. Criando ambiente virtual: `python3 -m venv venv`
   2. Ativando o ambiente virtual: `source venv/bin/activate`
   3. Instale as bibliotecas: `pip install -r requirements.txt`
4. Execute o Astronomer:
   1. CMD: `astro dev start`
   2. Abra o navegador e acesse: http://localhost:8080

5. Executar a DAG:
   1. Na interface do Airflow, ative a DAG `extract_data_dag` e aguarde sua execução.

6. Encerre a execução:
   1. CMD: `astro dev stop`
