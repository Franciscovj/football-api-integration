import pandas as pd
import json
import os

class DataHandler:

    @staticmethod
    def load_json(name_file):
        with open(f"json_files/{name_file}.json", "r") as file:
            player_data = json.load(file)
        return player_data

    @staticmethod
    def concat_data(data):
        df_final = pd.concat(data, ignore_index=True)
        return df_final

    @staticmethod
    def last_games_player(df, i, coluna, total):
        df_filtered = df[df[coluna] == i]
        df_last_10 = df_filtered.tail(total)
        return df_last_10

    @staticmethod
    def save_excel(data_frame, arquivo, dir):
        diretorio = dir
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        data_frame.to_excel(os.path.join(diretorio, arquivo), index=False)

    @staticmethod
    def save_csv(data_frame, arquivo, dir):
        diretorio = dir
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        if not pd.api.types.is_datetime64_any_dtype(data_frame['date']):
            data_frame['date'] = pd.to_datetime(data_frame['date'])
        
        data_frame['date'] = data_frame['date'].dt.strftime('%Y-%m-%d')
        
        data_frame.to_csv(os.path.join(diretorio, arquivo), index=False)


    @staticmethod
    def create_dir(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
                  
            
    @staticmethod        
    def save_list_to_txt(file_name, data_list,df):
        with open(file_name, 'w') as f:
            for item in data_list:
                f.write(f"{item}\n")

        liga_concat_unique = list(df["liga_concat"].unique())
        return liga_concat_unique        
