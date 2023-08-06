from django.contrib.auth import get_user_model

from calender.models import Event, Register
from films.models import Film


def get_schedule():
    """Return a list of (Event, Film) based on votes and the register."""
    event = Event.objects.future_events().first()
    if not event:
        return (None, None, None, None, None)

    present_users = set(
        register.user for register in Register.objects.present_for(event)
    )
    absent_users = set(register.user for register in Register.objects.absent_for(event))
    unknown_users = set(get_user_model().objects.all()) - present_users - absent_users

    film = preferred_film(event, present_users)
    return (event, film, present_users, absent_users, unknown_users)


def preferred_film(event, present_users):
    """Return the preferred film for the given event."""
    films = films_by_score(present_users)
    return films[0]


def films_by_score(present_users):
    films = (
        Film.objects.potentially_watchable()
        .prefetch_related("vote_set")
        .prefetch_related("vote_set__user")
    )
    if not films:
        return [None]

    score_films(films, present_users)
    return sorted(films, key=lambda x: (-x._schedule_score, x.id))


def score_films(films, present_users):
    for film in films:
        score_film(film, present_users)


def score_film(film, present_users):
    film._schedule_score = 0
    for vote in film.vote_set.all():
        score = vote.choice
        if vote.user in present_users:
            film._schedule_score += score
        else:
            film._schedule_score -= score
