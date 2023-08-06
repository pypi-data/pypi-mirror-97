import requests

from films.core import types

RATING_REPLACEMENTS = {
    "G": "U",
    "PG-13": "12",
    "TV-MA": "18",  # Compromise between 15 and 18
    "R": "18",
}


def get_film(api_key, url: str) -> types.Film:
    url = normalise_url(url)
    if not url.startswith("https://www.imdb.com/title/"):
        raise ValueError("Must be a direct link to a specific IMDB film")

    imdb_id = url[len("https://www.imdb.com/title/") :].partition("/")[0]

    response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}")
    response.raise_for_status()
    json = response.json()

    title = json["Title"]
    year = int(json["Year"])

    age_rating = _age_rating(json["Rated"])
    imdb_rating = _imdb_rating(json["imdbRating"])
    genre = json["Genre"]
    runtime_mins = None
    if "min" in json["Runtime"]:
        runtime_mins = int(json["Runtime"].split()[0])
    plot = json["Plot"]
    poster_url = json["Poster"]

    return types.Film(
        imdb=url,
        title=title,
        year=year,
        imdb_rating=imdb_rating,
        imdb_age=age_rating,
        genre=genre,
        runtime_mins=runtime_mins,
        plot=plot,
        poster_url=poster_url,
    )


def normalise_url(url):
    if url.startswith("https://m.imdb.com"):
        url = url[len("https://m.imdb.com") :]
        url = "https://www.imdb.com" + url
    return url


def _age_rating(rating: str) -> types.AgeRating:
    if rating.lower() in ("not rated", "n/a"):
        return None

    for original, replacement in RATING_REPLACEMENTS.items():
        if rating == original:
            return types.AgeRating(replacement)

    return types.AgeRating(rating)


def _imdb_rating(rating: str):
    if rating == "N/A":
        return None

    return float(rating)
