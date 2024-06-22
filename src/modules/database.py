import sqlite3
import os

class DatabaseConnector:

    @staticmethod
    def connect_bd(df, tabela, padrao):
        conn = sqlite3.connect("data/api_futebol.db")
        df.to_sql(tabela, conn, if_exists=padrao, index=False)
        conn.commit()
        conn.clos

    @staticmethod
    def execute_query(conn, query):
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()

    @staticmethod
    def fetch_existing_ids(conn, id, table_name):
        query = f"SELECT {id} FROM {table_name}"
        cursor = conn.cursor()
        cursor.execute(query)
        existing_ids = set(row[0] for row in cursor.fetchall())
        return existing_ids
    
    @staticmethod
    def create_dir_and_db(dir, db_name="api_futebol.db"):
        # Criar o diretório se ele não existir
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        # Caminho completo para o arquivo de banco de dados
        db_path = os.path.join(dir, db_name)
        
        # Criar o arquivo de banco de dados se ele não existir
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            conn.close()
            print(f"Banco de dados criado em: {db_path}")
        else:
            print(f"O banco de dados já existe em: {db_path}")  
