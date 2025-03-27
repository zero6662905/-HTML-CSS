import requests

url = "https://akabab.github.io/superhero-api/api/all.json"
response = requests.get(url)

if response.status_code == 200:
    heroes = response.json()
    for hero in heroes[:5]:
        print(f"Ім'я: {hero['name']}")
        print(f"slug: {hero['slug']}")
        print(f"Сили: {hero['powerstats']}\n")
else:
    print("Не вдалося отримати дані про героїв.")