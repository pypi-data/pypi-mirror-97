import logging

from bbfcapi.api_sync import best_match
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from films.clients import omdb
from films.core import types
from films.models import Film

logger = logging.getLogger(__name__)


class FilmCreate(SuccessMessageMixin, CreateView):
    model = Film
    fields = ["imdb", "is_available"]
    success_message = "You have added a new film."

    def form_valid(self, form):
        self.object = form.save(commit=False)

        _update_django_film_from_external(self.object)

        try:
            return super().form_valid(form)
        except IntegrityError:
            # We cannot determine which constraint failed as the error text varies
            # depending on the database backend, so we will rely on the get query.
            # If the film exists despite the IntegrityError, then it was a unique
            # constraint violation - the film has already been added.
            try:
                self.object = Film.objects.get(
                    title=self.object.title, year=self.object.year
                )
                return HttpResponseRedirect(self.get_success_url())
            except Film.DoesNotExist:
                pass
            raise

    def get_success_url(self):
        if "_save" in self.request.POST:
            return reverse("votes:vote-create")
        elif "_edit" in self.request.POST:
            return super().get_success_url()
        elif "_addanother" in self.request.POST:
            return reverse("films:film-create")


class FilmUpdate(SuccessMessageMixin, UpdateView):
    model = Film
    fields = [
        "title",
        "imdb",
        "year",
        "imdb_age",
        "bbfc_age",
        "imdb_rating",
        "genre",
        "runtime_mins",
        "plot",
        "poster_url",
        "trailer",
        "is_available",
        "is_watched",
    ]
    success_message = "You have updated the film %(title)s."

    def get_success_url(self):
        if "_save" in self.request.POST:
            return reverse("votes:vote-aggregate")
        elif "_edit" in self.request.POST:
            return super().get_success_url()
        elif "_addanother" in self.request.POST:
            return reverse("films:film-create")


class FilmRefresh(SingleObjectMixin, View):
    model = Film
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        film = self.get_object()
        _update_django_film_from_external(film)
        film.save()
        messages.success(self.request, f"{film.title} has been refreshed.")
        return HttpResponseRedirect(
            reverse("films:film-update", kwargs={"pk": film.pk})
        )


def _update_django_film_from_external(dfilm: Film) -> None:
    cfilm = omdb.get_film(settings.OMDB_API_KEY, dfilm.imdb)
    try:
        bbfc_age = best_match(cfilm.title).age_rating
        bbfc_age = types.AgeRating(bbfc_age.value)
    except:
        logger.exception("Failed to get BBFC age rating.")
        bbfc_age = None

    dfilm.title = cfilm.title
    dfilm.year = cfilm.year
    dfilm.imdb_age = cfilm.imdb_age.value if cfilm.imdb_age else dfilm.imdb_age
    dfilm.bbfc_age = bbfc_age.value if bbfc_age else dfilm.bbfc_age
    dfilm.imdb_rating = cfilm.imdb_rating
    dfilm.genre = cfilm.genre
    dfilm.runtime_mins = cfilm.runtime_mins
    dfilm.plot = cfilm.plot
    dfilm.poster_url = cfilm.poster_url
    return dfilm
