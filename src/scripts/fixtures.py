import sys
sys.path.append('./src')
from modules.database import DatabaseConnector
from modules.conect_api import APIClient
from modules.data_handling import DataHandler
from utils.config import ligalista
import pandas as pd
import json
import sqlite3

from dotenv import load_dotenv
load_dotenv()  
import os
api_key = os.getenv("API_KEY")


from_date = "2023-12-31"
to_date = "2024-06-17"

api_client = APIClient(api_key = api_key)
DatabaseConnector.create_dir_and_db("data")

query = ('''
    CREATE TABLE IF NOT EXISTS dados_fixtures (
        id_jogo INTEGER PRIMARY KEY,
        date TEXT,
        id_liga INTEGER,
        liga TEXT,
        pais TEXT,
        status TEXT,
        home TEXT,
        away TEXT,
        home_gols INTEGER,
        away_gols INTEGER
    )
    ''')

conn = sqlite3.connect('data/api_futebol.db')
DatabaseConnector.execute_query(conn, query)
existing_ids = DatabaseConnector.fetch_existing_ids(conn, 'id_jogo', 'dados_fixtures')

total_new_records = 0
new_records_list = []

for liga in ligalista:    
    api_client.fetch_fixtures(league=liga, from_date=from_date, to_date=to_date, season="2024")
    json_data = DataHandler.load_json('fixtures')
    if json_data["response"]:
        dados = []

        for elemento in json_data["response"]:
            jogoid = elemento['fixture']
            time = elemento["teams"]
            placar = elemento["score"]
            liga = elemento["league"]
            dados_elemento = {
                "id_jogo": jogoid["id"],
                "date": jogoid['date'],
                "id_liga": liga["id"],
                "liga": liga["name"],
                "pais": liga["country"],
                "status": jogoid["status"]["short"],
                "home": time["home"]["name"],
                "away": time["away"]["name"],
                "home_gols": placar["fulltime"]["home"],
                "away_gols": placar["fulltime"]["away"]
            }

            dados.append(dados_elemento)

        df = pd.DataFrame(dados)
        new_records = df[~df['id_jogo'].isin(existing_ids)]
        
        if not new_records.empty:
            new_records.to_sql('dados_fixtures', conn, if_exists='append', index=False)
            new_records_list.extend(new_records.to_dict(orient='records'))
            total_new_records += len(new_records)
        else:
            print("Nenhum registro novo para inserir.")

if total_new_records > 0:
    with open('json_files/new_records.json', 'w') as f:
        json.dump(new_records_list, f, indent=4)
    print(f"{total_new_records} registros foram inseridos.")
else:
    print("Nenhum registro novo para inserir.")

print(f"total ligas: {len(ligalista)}")
conn.close()
