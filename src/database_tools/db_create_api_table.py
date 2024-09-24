# src/database_tools/db_create_api_table.py

import os
import psycopg2
from psycopg2 import sql
import pandas as pd
from dotenv import load_dotenv
from psycopg2.extensions import quote_ident

class DatabaseTools:
    def __init__(self):
        # Carrega as variáveis do arquivo .env
        load_dotenv()

        # Configurações do banco de dados utilizando variáveis de ambiente
        DB_CONFIG = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT"))
        }

        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, data):
        """
        Cria uma tabela no banco de dados PostgreSQL com base nos dados extraídos e insere os dados na tabela.

        Args:
            table_name (str): Nome da tabela a ser criada.
            data (list[dict]): Dados para determinar o schema da tabela.

        Returns:
            None
        """
        # Convertendo os dados para um DataFrame para inferir os tipos de dados
        df = pd.DataFrame(data)

        # Gerando o schema da tabela com base no DataFrame
        columns = []
        for column_name, dtype in zip(df.columns, df.dtypes):
            if pd.api.types.is_integer_dtype(dtype):
                column_type = "INTEGER"
            elif pd.api.types.is_float_dtype(dtype):
                column_type = "FLOAT"
            elif pd.api.types.is_bool_dtype(dtype):
                column_type = "BOOLEAN"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_type = "TIMESTAMP"
            else:
                column_type = "TEXT"

            # Usando quote_ident para garantir que os identificadores de colunas sejam tratados corretamente
            columns.append(sql.SQL(quote_ident(column_name, self.connection)) + sql.SQL(" ") + sql.SQL(column_type))

        # Criando a query de criação da tabela
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(columns)
        )

        # Executando a query de criação da tabela
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print(f"Tabela '{table_name}' criada com sucesso.")

        # Inserindo os dados na tabela
        self.insert_data(table_name, df)

    def insert_data(self, table_name, df):
        """
        Insere os dados no banco de dados PostgreSQL.

        Args:
            table_name (str): Nome da tabela onde os dados serão inseridos.
            df (DataFrame): Dados a serem inseridos.

        Returns:
            None
        """
        # Gerando a query de inserção
        columns = sql.SQL(", ").join(map(sql.Identifier, df.columns))
        values = sql.SQL(", ").join(sql.Placeholder() * len(df.columns))

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            columns,
            values
        )

        # Inserindo os dados linha por linha
        for row in df.itertuples(index=False, name=None):
            try:
                self.cursor.execute(insert_query, row)
            except psycopg2.Error as e:
                print(f"Erro ao inserir dados na tabela '{table_name}': {e}")
                self.connection.rollback()
                raise

        self.connection.commit()
        print(f"Dados inseridos na tabela '{table_name}' com sucesso.")

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.cursor.close()
        self.connection.close()
        print("Conexão com o banco de dados encerrada.")