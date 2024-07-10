import requests
import json
import os


class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
            "x-rapidapi-key": api_key,
        }

    def fetch_fixtures(self, league, from_date, to_date, season):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"league": league, "from": from_date, "to": to_date, "season": season}
        response = requests.get(url, headers=self.headers, params=params)
        self.save_response(response, "fixtures")

    def fetch_leagues(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
        response = requests.get(url, headers=self.headers)
        self.save_response(response, "ligas_id")

    def fetch_stats(self, fixture_id):
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics?fixture={fixture_id}"
        response = requests.get(url, headers=self.headers)
        return response
        

    def save_response(self, response, filename):
        try:
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                if not os.path.exists("json_files"):
                    os.makedirs("json_files")
                filepath = f"json_files/{filename}.json"
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Exemplo de uso:
# api_key = "sua_api_key_aqui"
# client = APIClient(api_key)
# client.fetch_fixtures(league_id, "2023-01-01", "2023-12-31", 2023)
# client.fetch_leagues()
# client.fetch_stats(fixture_id)
