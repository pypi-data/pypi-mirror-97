from films.models import Film
from votes.models import Vote


def next_film_to_vote(user):
    return films_to_vote(user).first()


def has_fully_voted(user):
    return not films_to_vote(user).exists()


def films_to_vote(user):
    return Film.objects.exclude(is_watched=True).exclude(
        pk__in=Vote.objects.filter(user=user).values_list("film")
    )
