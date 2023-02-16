import requests

KEY = 'fbb315277915128a7e9f0af1e7ac6fdf'
query = 'Titanic'

API_URL = f"https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={query}"
response = requests.get(API_URL)
response_json = response.json()
results = response_json['results']
final = len(results)
for i in range(0, final):
    print(results[i]['poster_path'])







