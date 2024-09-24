# datasources/endpoints/carros_modelos_por_ano.py

from src.api_utils.api_connection import BaseConnector
import pandas as pd
import numpy as np
import time
import os
import json

class RequestModelosPorAno(BaseConnector):
    def __init__(self, url):
        super().__init__(url)

    @BaseConnector.request_post()
    def get_table(self, response, *args, **kwargs):
        return response

    def get_tabela_carros_modelos_por_ano(self):
        df_modelos = pd.read_json('storage/raw/carros_modelos.json')
        partes = np.array_split(df_modelos, 500)
        resultado_final = []
        diretorio_partes = 'storage/raw/partes_modelos_por_ano'
        os.makedirs(diretorio_partes, exist_ok=True)

        for i, parte in enumerate(partes):
            print(f"Processando parte {i+1} de 500.")
            resultados_tipos_veiculo = []
            for _, row in parte.iterrows():
                payload = {
                    "codigoTabelaReferencia": 312,
                    "codigoTipoVeiculo": 1,
                    "codigoMarca": row['codigoMarca'],
                    "codigoModelo": row['Value'],
                }
                try:
                    response = self.get_table(data=payload)
                    resultados_tipos_veiculo.append(response)
                except Exception as e:
                    print(f"Erro ao processar modelo {row['Value']} da marca {row['codigoMarca']}: {e}")
                    resultados_tipos_veiculo.append(None)
                time.sleep(1.5)

            parte['ResultadoTiposVeiculo'] = resultados_tipos_veiculo
            resultado_final.extend(parte.to_dict(orient='records'))
            parte.to_json(os.path.join(diretorio_partes, f'resultados_tipos_veiculo_part{i+1}.json'), orient='records', force_ascii=False, indent=4)
            print(f"Parte {i+1} salva com sucesso.")

        diretorio_final = 'storage/raw'
        os.makedirs(diretorio_final, exist_ok=True)
        with open(os.path.join(diretorio_final, 'resultados_tipos_veiculo_final.json'), 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, ensure_ascii=False, indent=4)
        
        print("Todos os dados foram salvos com sucesso.")
