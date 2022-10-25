import requests

MOVIE_DB_KEY = "7927df2168a99c50b7ac292d26255796"
parameters = {
    "api_key": MOVIE_DB_KEY,
    "query": "spirited away",
    # "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
movies_online_dtb = "https://api.themoviedb.org/3/search/movie"


suggested_films = requests.get(movies_online_dtb, params=parameters).json()["results"]
print(suggested_films)
params = {
    "api_key": MOVIE_DB_KEY,
}
movie = requests.get("https://api.themoviedb.org/3/movie/129", params=params).json()
print(movie)
poster = requests.get("https://api.themoviedb.org/3/movie/624860/8c4a8kE7PizaGQQnditMmI1xbRp.jpg", params=params).json()
print(poster)