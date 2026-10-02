import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from config import STEAM_API_KEY, STEAM_ID
from get_library import get_owned_games

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_game_reviews(game):
    appid = game["appid"]
    name = game["name"]
    cursor = "*"
    pages = 0
    reviews = []

    while True:
        try:
            response = requests.get(
                f"https://store.steampowered.com/appreviews/{appid}",
                params={
                    "json": 1,
                    "filter": "all",
                    "language": "english",
                    "review_type": "all",
                    "num_per_page": 100,
                    "cursor": cursor,
                },
                headers=HEADERS
            )
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {name} ({appid}): {e}")
            break

        if response.status_code != 200:
            print(f"Non-200 status for {name} ({appid}): {response.status_code}")
            break
        
        data = response.json()
        if data.get("success") != 1:
            print(f"Steam returned an error for {name} ({appid})")
            break

        for review in data["reviews"]:
            reviews.append({
                "name": name,
                "voted_up": review["voted_up"],
                "hours_played": review["author"]["playtime_forever"] / 60,
                "text": review["review"],
            })

        pages += 1
        if pages >= 3:
            break
        if not data["reviews"] or data["cursor"] == cursor:
            break
        cursor = data["cursor"]
        time.sleep(1)

    return reviews


def main():
    games = get_owned_games(STEAM_API_KEY, STEAM_ID)
    filename = "reviews.json"
    collected = []

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(fetch_game_reviews, game): game for game in games}
        for future in as_completed(futures):
            game = futures[future]
            try:
                reviews = future.result()
                collected.extend(reviews)
                print(f"Done: {game['name']} ({len(reviews)} reviews)")
            except Exception as e:
                print(f"Failed on {game['name']}: {e}")

    if os.path.exists(filename):
        os.remove(filename)
    for review in collected:
        write_review_to_file(review, filename=filename)


def write_review_to_file(review, filename):
    with open(filename, "a") as f:
        json.dump(review, f)
        f.write("\n")


if __name__ == "__main__":
    main()