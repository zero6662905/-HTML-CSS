import requests
import json

url = "https://api.jikan.moe/v4/top/anime"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    popular_anime = []

    for anime in data['data']:
        anime_info = {
            "title": anime['title'],
            "score": anime['score']
        }
        popular_anime.append(anime_info)

    with open('popular_anime.json', 'w', encoding='utf-8') as f:
        json.dump(popular_anime, f, ensure_ascii=False, indent=4)

    print("Дані успішно збережено у popular_anime.json")
else:
    print(f"Помилка запиту: {response.status_code}")