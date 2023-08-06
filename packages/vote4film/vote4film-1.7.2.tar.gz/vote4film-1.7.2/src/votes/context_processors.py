from votes.logic import next_film_to_vote


def is_vote_available(request):
    if not request.user.is_authenticated:
        return {}

    return {"is_vote_available": bool(next_film_to_vote(request.user))}
