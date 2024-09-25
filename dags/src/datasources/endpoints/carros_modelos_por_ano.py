# src/datasources/endpoints/carros_modelos_por_ano.py
# Classe para obter os modelos de carros por ano.

from src.api_utils.api_connection import BaseConnector
import pandas as pd
import numpy as np
import time
import os
import json
import logging
from src.api_utils.api_config import CODIGO_TABELA_REFERENCIA

class RequestModelosPorAno(BaseConnector):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)

    def get_tabela_carros_modelos_por_ano(self):
        df_modelos = pd.read_json('data/raw/carros_modelos.json')
        partes = np.array_split(df_modelos, 500)
        diretorio_partes = 'data/raw/partes_modelos_por_ano'
        os.makedirs(diretorio_partes, exist_ok=True)

        for i, parte in enumerate(partes):
            logging.info(f"Processando parte {i+1} de {len(partes)}.")
            resultados_tipos_veiculo = []
            for _, row in parte.iterrows():
                payload = {
                    "codigoTabelaReferencia": CODIGO_TABELA_REFERENCIA,
                    "codigoTipoVeiculo": 1,
                    "codigoMarca": row['codigoMarca'],
                    "codigoModelo": row['Value'],
                }
                response = self.post(data=payload)
                if response:
                    resultados_tipos_veiculo.append(response)
                else:
                    logging.error(f"Erro ao processar modelo {row['Value']} da marca {row['codigoMarca']}")
                    resultados_tipos_veiculo.append(None)
                time.sleep(self.delay)
            parte['ResultadoTiposVeiculo'] = resultados_tipos_veiculo
            parte.to_json(
                os.path.join(diretorio_partes, f'resultados_tipos_veiculo_part{i+1}.json'),
                orient='records', force_ascii=False, indent=4
            )
            logging.info(f"Parte {i+1} salva com sucesso.")

        logging.info("Todos os dados foram salvos com sucesso.")
