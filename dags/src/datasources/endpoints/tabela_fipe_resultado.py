# src/datasources/endpoints/tabela_fipe_resultado.py
# Classe para obter os resultados da tabela FIPE para cada veículo.

import pandas as pd
import numpy as np
import time
import os
import ast
import logging
from src.api_utils.api_connection import BaseConnector
from src.api_utils.api_config import CODIGO_TABELA_REFERENCIA

class RequestFipeResultado(BaseConnector):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)

    def transforming_dataframe(self):
        """
        Transforma o DataFrame de resultados brutos em um formato expandido,
        contendo as informações dos veículos e seus respectivos anos e combustíveis.
        """
        df = pd.read_csv('data/raw/resultados_tipos_veiculo_completo.csv')
        df.rename(columns={
            "Label": "nome_veiculo",
            "Value": "cod_veiculo",
            "codigoMarca": "cod_marca",
            "ResultadoTiposVeiculo": "cod_veiculo_especifico"
        }, inplace=True)

        expanded_rows = []
        for _, row in df.iterrows():
            try:
                cod_veiculo_especifico_list = ast.literal_eval(row['cod_veiculo_especifico'])
            except (ValueError, SyntaxError):
                continue

            if isinstance(cod_veiculo_especifico_list, list):
                for veiculo_especifico in cod_veiculo_especifico_list:
                    if isinstance(veiculo_especifico, dict):
                        expanded_rows.append({
                            "nome_veiculo": row['nome_veiculo'],
                            "cod_veiculo": row['cod_veiculo'],
                            "cod_marca": row['cod_marca'],
                            "Label": veiculo_especifico.get('Label', ''),
                            "Value": veiculo_especifico.get('Value', '')
                        })

        expanded_df = pd.DataFrame(expanded_rows)
        expanded_df[['Ano', 'Combustivel']] = expanded_df['Label'].str.split(' ', expand=True)
        expanded_df['cod_combustivel'] = expanded_df['Value'].str.split('-').str[1]
        expanded_df.rename(columns={"Label": "ano_combustivel", "Value": "ano_cod_combustivel"}, inplace=True)
        self.expanded_df = expanded_df

    def get_tabela_de_resultado_fipe(self):
        """
        Processa os dados da tabela FIPE, dividindo em partes e realizando requisições para cada modelo e veículo específico.
        """
        self.transforming_dataframe()
        partes_tabela_fipe = np.array_split(self.expanded_df, 500)

        # Verifica partes já processadas
        diretorio_partes = 'data/raw/partes_resultado'
        os.makedirs(diretorio_partes, exist_ok=True)

        arquivos_existentes = [
            int(f.split('resultado_tabela_fipe')[1].split('.csv')[0])
            for f in os.listdir(diretorio_partes)
            if f.startswith('resultado_tabela_fipe') and f.endswith('.csv')
        ]
        ultima_parte_processada = max(arquivos_existentes) if arquivos_existentes else 0

        for i, parte in enumerate(partes_tabela_fipe):
            if i + 1 <= ultima_parte_processada:
                logging.info(f"Parte {i+1} já processada, pulando.")
                continue

            logging.info(f"Processando parte {i+1}.")
            resultados_tabela_fipe = []
            for _, row in parte.iterrows():
                payload = {
                    "codigoTabelaReferencia": CODIGO_TABELA_REFERENCIA,
                    "codigoTipoVeiculo": 1,
                    "codigoMarca": row['cod_marca'],
                    "codigoModelo": row['cod_veiculo'],
                    "anoModelo": row['Ano'],
                    "codigoTipoCombustivel": row['cod_combustivel'],
                    "tipoVeiculo": "carro",
                    "tipoConsulta": "tradicional"
                }

                # Realiza a requisição e tenta novamente em caso de erro
                response = self._retry_request(payload)
                resultados_tabela_fipe.append(response)

            # Salva os resultados da parte processada
            if resultados_tabela_fipe:
                parte['ResultadoTabelaFipe'] = resultados_tabela_fipe
                parte.to_csv(
                    os.path.join(diretorio_partes, f'resultado_tabela_fipe{i+1}.csv'),
                    index=False
                )
                logging.info(f"Parte {i+1} salva com sucesso.")

        logging.info("Processamento concluído.")

    def _retry_request(self, payload, max_retries=5):
        """
        Realiza a requisição com várias tentativas em caso de erro, utilizando a lógica de backoff.
        """
        response = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self.post(data=payload)
                if response and isinstance(response, dict):
                    return response
            except Exception as e:
                if attempt == max_retries:
                    logging.error(f"Erro ao processar: {e}. Máximo de tentativas alcançado.")
                    return None
                wait_time = min(5, 1.5 * 2 ** (attempt - 1))
                logging.warning(f"Erro na tentativa {attempt}. Aguardando {wait_time} segundos.")
                time.sleep(wait_time)
        return None
