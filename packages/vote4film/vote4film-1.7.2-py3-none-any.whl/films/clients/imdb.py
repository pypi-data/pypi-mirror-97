import requests
from lxml import html  # nosec

from films.core import types


def get_film(url: str) -> types.Film:
    if not url.startswith("https://www.imdb.com/title/"):
        raise ValueError("Must be a direct link to a specific IMDB film")

    response = requests.get(url)
    response.raise_for_status()
    tree = html.fromstring(response.content)

    title = tree.xpath("//h1/text()")[0].strip()
    year = int(tree.xpath('//span[@id="titleYear"]/a/text()')[0])
    age_rating = types.AgeRating(
        tree.xpath('//div[@class="subtext"]/text()')[0].strip()
    )
    imdb_rating = float(tree.xpath('//span[@itemprop="ratingValue"]/text()')[0])

    return types.Film(
        imdb=url,
        title=title,
        year=year,
        imdb_age=age_rating,
        imdb_rating=imdb_rating,
    )
