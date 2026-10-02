import json
import os
import time
from urllib import response
import requests
from config import STEAM_API_KEY, STEAM_ID
from get_library import get_owned_games

def main(): 

    games = get_owned_games(STEAM_API_KEY, STEAM_ID)
    filename="reviews.json"
    collected = []
    game_counter = 0
    for game in games:
        appid = game["appid"]
        name = game["name"]
        cursor = "*"
        pages = 0
        if game_counter >= 2:  # Limit the number of games to scrape
            break

        while True:
           
            try:
                response = requests.get(
                    f"https://store.steampowered.com/appreviews/{appid}",
                    params={
                        "json": 1,
                        "filter": "all",
                        "language": "english",
                        "review_type": "all",
                        "num_per_page": 5,
                        "cursor": cursor,  # '*' means "start from the beginning"
                    },
                )
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break
        
            
            data = response.json()
            if data.get("success") != 1:
                    print(f"Steam returned an error for appid {appid}")
                    break
            for review in data["reviews"]:
                collected.append({
                    "name": name,
                    "voted_up": review["voted_up"],
                    "hours_played": review["author"]["playtime_forever"] / 60,
                    "text": review["review"],
                })
            
            pages += 1
            if pages >= 2:  # Limit the number of pages to scrape
                break
            if not data["reviews"] or data["cursor"] == cursor:
                break
            cursor = data["cursor"]
            time.sleep(1)  # Be polite and avoid hitting the server too hard

        game_counter += 1

    if os.path.exists(filename):
        os.remove(filename)  # Remove the file if it exists to avoid appending to old data
    for review in collected:
        
        write_review_to_file(review, filename=filename)

def write_review_to_file(review, filename):
    with open(filename, "a") as f:
        json.dump(review, f)
        f.write("\n")  # Write each review
if __name__ == "__main__":
    main()