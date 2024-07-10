import sys
sys.path.append('./src')
from modules.database import DatabaseConnector
from modules.conect_api import APIClient
from modules.data_handling import DataHandler
from utils.config import ligalista
import pandas as pd
from tqdm import tqdm
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()  
api_key = os.getenv("API_KEY")

api_client = APIClient(api_key=api_key)
DatabaseConnector.create_dir_and_db("data")

def obter_estatisticas(fixture_id):
    response = api_client.fetch_stats(fixture_id)
    if response.status_code == 200:
        data_stats = response.json().get("response", [])
        if data_stats and len(data_stats) >= 2:
            home_stats = data_stats[0]["statistics"]
            away_stats = data_stats[1]["statistics"]
            return home_stats, away_stats
    return None, None

from_date = "2023-12-31"
to_date = "2024-07-09"

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
            new_records_list.extend(new_records['id_jogo'].tolist())

if new_records_list:
    all_stat_columns = set()
    stat_data = []

    for fixture_id in tqdm(new_records_list, desc="Fetching Stats"):
        home_stats, away_stats = obter_estatisticas(fixture_id)
        if home_stats and away_stats:
            home_stats_dict = {f"home_{stat['type'].replace(' ', '_')}": stat['value'] for stat in home_stats}
            away_stats_dict = {f"away_{stat['type'].replace(' ', '_')}": stat['value'] for stat in away_stats}
            home_stats_dict["Fixture_ID"] = fixture_id
            away_stats_dict["Fixture_ID"] = fixture_id
            all_stat_columns.update(home_stats_dict.keys())
            all_stat_columns.update(away_stats_dict.keys())
            stat_data.append({**home_stats_dict, **away_stats_dict})

    if stat_data:
        df_stats = pd.DataFrame(stat_data, columns=sorted(all_stat_columns))
        df_stats.to_sql('dados_stats', conn, if_exists='append', index=False)
        print(f"{len(stat_data)} registros foram inseridos em 'dados_stats'.")
    else:
        print("Nenhum dado de estatísticas foi inserido.")
else:
    print("Nenhum registro novo para inserir.")

print(f"Total de ligas: {len(ligalista)}")
conn.close()
