# datasources/endpoints/tabela_fipe_resultado.py

from src.api_utils.api_connection import BaseConnector
import pandas as pd
import numpy as np
import time
import os
import ast

class RequestFipeResultado(BaseConnector):
    def __init__(self, url):
        super().__init__(url)

    @BaseConnector.request_post()
    def get_table(self, response, *args, **kwargs):
        return response

    def transforming_dataframe(self):
        df = pd.read_csv('storage/raw/resultados_tipos_veiculo_completo.csv')
        df.rename(columns={
            "Label": "nome_veiculo",
            "Value": "cod_veiculo",
            "codigoMarca": "cod_marca",
            "ResultadoTiposVeiculo": "cod_veiculo_especifico"
        }, inplace=True)
        expanded_rows = []
        for idx, row in df.iterrows():
            nome_veiculo = row['nome_veiculo']
            cod_veiculo = row['cod_veiculo']
            cod_marca = row['cod_marca']
            try:
                cod_veiculo_especifico_list = ast.literal_eval(row['cod_veiculo_especifico'])
            except (ValueError, SyntaxError):
                continue
            if isinstance(cod_veiculo_especifico_list, list):
                for veiculo_especifico in cod_veiculo_especifico_list:
                    if isinstance(veiculo_especifico, dict):
                        expanded_rows.append({
                            "nome_veiculo": nome_veiculo,
                            "cod_veiculo": cod_veiculo,
                            "cod_marca": cod_marca,
                            "Label": veiculo_especifico.get('Label', ''),
                            "Value": veiculo_especifico.get('Value', '')
                        })
        expanded_df = pd.DataFrame(expanded_rows)
        expanded_df[['Ano', 'Combustivel']] = expanded_df['Label'].str.split(' ', expand=True)
        expanded_df['cod_combustivel'] = expanded_df['Value'].str.split('-').str[1]
        expanded_df.rename(columns={
            "Label": "ano_combustivel",
            "Value": "ano_cod_combustivel"
        }, inplace=True)
        self.expanded_df = expanded_df

    def get_tabela_de_resultado_fipe(self):
        self.transforming_dataframe()
        partes_tabela_fipe = np.array_split(self.expanded_df, 500)
        arquivos_existentes = [
            int(f.split('resultado_tabela_fipe')[1].split('.csv')[0])
            for f in os.listdir('storage/raw/partes_resultado/')
            if f.startswith('resultado_tabela_fipe') and f.endswith('.csv')
        ]
        ultima_parte_processada = max(arquivos_existentes) if arquivos_existentes else 0
        for i, parte in enumerate(partes_tabela_fipe):
            if i + 1 <= ultima_parte_processada:
                print(f"Parte {i+1} já processada, pulando.")
                continue
            print(f"Processando parte {i+1}.")
            resultados_tabela_fipe = []
            for _, row in parte.iterrows():
                payload = {
                    "codigoTabelaReferencia": 312,
                    "codigoTipoVeiculo": 1,
                    "codigoMarca": row['cod_marca'],
                    "codigoModelo": row['cod_veiculo'],
                    "anoModelo": row['Ano'],
                    "codigoTipoCombustivel": row['cod_combustivel'],
                    "tipoVeiculo": "carro",
                    "tipoConsulta": "tradicional"
                }
                retries = 5
                response = None
                for attempt in range(1, retries + 1):
                    try:
                        response = self.get_table(data=payload)
                        if response is not None and isinstance(response, dict):
                            resultados_tabela_fipe.append(response)
                            break
                    except Exception as e:
                        if attempt == retries:
                            print(f"Erro ao processar modelo {row['cod_veiculo']} da marca {row['cod_marca']}: {e}.")
                            resultados_tabela_fipe.append(None)
                        else:
                            wait_time = 1.5 if attempt == 1 else min(5, 1.2 * 2 ** (attempt - 1))
                            print(f"Erro 429: tentativa {attempt}. Aguardando {wait_time} segundos.")
                            time.sleep(wait_time)
                time.sleep(1.5)
            if resultados_tabela_fipe:
                parte['ResultadoTabelaFipe'] = resultados_tabela_fipe
                parte.to_csv(f'storage/raw/partes_resultado/resultado_tabela_fipe{i+1}.csv', index=False)
                print(f"Parte {i+1} salva com sucesso.")
        print("Processamento concluído.")
