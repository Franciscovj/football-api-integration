import sys
sys.path.append('./src')
from modules.conect_api import APIClient
from modules.data_handling import DataHandler
from modules.database import DatabaseConnector
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()  

api_key = os.getenv("API_KEY")
api_client = APIClient(api_key = api_key)

DatabaseConnector.create_dir_and_db("data")

conn = sqlite3.connect("data/api_futebol.db")

api_client.fetch_leagues()
json_data = DataHandler.load_json('ligas_id')

if json_data["response"]:

    dados = []

    for elemento in json_data["response"]:
        liga = elemento["league"]
        pais = elemento["country"]

        dados_elemento = {
            "id_liga": liga["id"],
            "nome_liga": liga["name"],
            "nome_pais": pais["name"],
            "codigo_pais": pais["code"],
        }

        dados.append(dados_elemento)

    df = pd.DataFrame(dados) 

    

    df.to_sql("dados_liga", conn, if_exists="replace", index=False)


conn.close()