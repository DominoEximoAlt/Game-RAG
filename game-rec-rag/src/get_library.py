import json
from urllib import response
import requests
from config import STEAM_API_KEY, STEAM_ID


def main(): 

    cursor = "*"
    response = requests.get(
                    f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}",
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
    for game in data["response"]["games"]:
        print(f"AppID: {game['appid']}, Name: {game['name']}, Playtime: {game['playtime_forever']} minutes")

    

if __name__ == "__main__":
    main()