import json
from urllib import response
import requests
from config import STEAM_API_KEY, STEAM_ID


def main(): 

    games = get_owned_games(STEAM_API_KEY, STEAM_ID)

    for game in games:
        print(f"Game Name: {game['name']}, App ID: {game['appid']}, Playtime: {game['playtime_forever']} minutes")

def get_owned_games(steam_api_key, steam_id):
    cursor = "*"
    response = requests.get(
                    f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_id}",
                    params={
                        "json": 1,
                        "filter": "all",
                        "language": "english",
                        "review_type": "all",
                        "num_per_page": 5,
                        "include_appinfo": 1,
                        "include_played_free_games": 1,
                        "cursor": cursor,
                    },
                )

    data = response.json()
    return data["response"]["games"]

    

if __name__ == "__main__":
    main()