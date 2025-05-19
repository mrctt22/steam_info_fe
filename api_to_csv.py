import requests
import csv
import json
import os

def fetch_api_data(url, params=None, headers=None):
    """
    Effettua una chiamata GET all'API e restituisce i dati in formato JSON.
    """
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_csv(data, filename):
    """
    Salva una lista di dizionari in un file CSV.
    """
    if not data:
        print("Nessun dato da salvare.")
        return
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Dati salvati in {filename}")

def save_to_json(data, filename):
    """
    Salva i dati in un file JSON.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dati salvati in {filename}")

def load_config(config_file):
    """
    Carica la configurazione da un file config.json.
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config('config/config.json')
    api_key = config.get('api_key')
    steam_id = config.get('steam_id')

    # Prima chiamata: GetPlayerSummaries
    try:
        url1 = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
        dati1 = fetch_api_data(url1)
        players = dati1.get('response', {}).get('players', [])
        save_to_json(players, "output/player_summaries.json")
    except Exception as e:
        print(f"Errore nella chiamata a GetPlayerSummaries: {e}")
        players = []

    # Seconda chiamata: GetOwnedGames
    try:
        url2 = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&include_appinfo=1&format=json"
        dati2 = fetch_api_data(url2)
        games = dati2.get('response', {}).get('games', [])
        save_to_json(games, "output/owned_games.json")
    except Exception as e:
        print(f"Errore nella chiamata a GetOwnedGames: {e}")
        games = []

    # Terza chiamata: GetUserStatsForGame per ogni appid
    # Disattivato il ciclo per GetUserStatsForGame
    # for game in games:
    #     appid = game.get('appid')
    #     if not appid:
    #         continue
    #     try:
    #         url3 = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={api_key}&steamid={steam_id}"
    #         stats = fetch_api_data(url3)
    #         save_to_json(stats, f"output/user_stats_{appid}.json")
    #     except Exception as e:
    #         print(f"Errore nella chiamata a GetUserStatsForGame per appid {appid}: {e}")
