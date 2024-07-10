import sys
sys.path.append('./src')
import pandas as pd
import sqlite3
from modules.data_handling import DataHandler

conn = sqlite3.connect("data/api_futebol.db")

dados_stats = "SELECT * FROM dados_stats"
df = pd.read_sql_query(dados_stats, conn)

df.rename(columns={'Fixture_ID': 'id_jogo'}, inplace=True)

dados_fixtures = "SELECT * FROM dados_fixtures"
dff = pd.read_sql_query(dados_fixtures, conn)

dff['liga_concat'] = dff['liga'] + '-' + dff['pais']

dfp = pd.merge(dff, df, on="id_jogo")

dfs = dfp.drop_duplicates(subset=["id_jogo"])

dfs['date'] = pd.to_datetime(dfs['date']).dt.tz_localize(None)

dfs = dfs.sort_values(by='date')

dfs.to_excel('jogos_full.xlsx', index=False)

conn.close()
