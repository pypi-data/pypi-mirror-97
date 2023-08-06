from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Prefetch, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from films.models import Film
from votes.forms import VoteForm
from votes.logic import next_film_to_vote
from votes.models import Vote


class NoMoreFilms(Exception):
    pass


class VoteCreate(SuccessMessageMixin, CreateView):
    model = Vote
    form_class = VoteForm
    success_message = "You have voted for %(film)s."

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except NoMoreFilms:
            messages.success(request, "There are no new films to vote for.")
            return redirect("web:home")

    def get_initial(self):
        # Set the film that we are voting for
        initial = super().get_initial()
        film = next_film_to_vote(self.request.user)
        if not film:
            raise NoMoreFilms("No more films to vote for")

        initial["film"] = film
        initial["user"] = self.request.user.pk
        return initial

    def get_form_kwargs(self):
        # Ensure form always has the current user present
        kwargs = super().get_form_kwargs()
        # Only have data when posting
        if "data" in kwargs:
            data = kwargs["data"].copy()
            data["user"] = self.request.user.pk
            kwargs["data"] = data

        return kwargs

    def get_context_data(self, **kwargs):
        # Provide easier access to film in the template
        context = super().get_context_data(**kwargs)
        context["film"] = context["form"].initial["film"]
        return context

    def form_valid(self, form):
        # Set the form's user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Continue reviewing if and only if there are cards to review
        if next_film_to_vote(self.request.user):
            return reverse("votes:vote-create")
        else:
            messages.success(self.request, "You have voted for all of the films.")
            return reverse("schedule:schedule")


class VoteUpdate(SuccessMessageMixin, UpdateView):
    model = Vote
    form_class = VoteForm
    success_url = reverse_lazy("votes:vote-aggregate")
    success_message = "Your vote for %(film)s was updated."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)  # Security
            .select_related("film")  # Performance
        )

    def get_context_data(self, **kwargs):
        # Provide easier access to film in the template
        context = super().get_context_data(**kwargs)
        context["film"] = context["form"].instance.film
        return context


class VoteAggregate(ListView):
    model = Film
    template_name = "votes/vote_aggregate.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                score=Coalesce(Sum("vote__choice"), Value(0)),
                has_user_voted=Count("vote", filter=Q(vote__user=self.request.user)),
            )
            .order_by("is_watched", "-score", "id")
            .prefetch_related(
                "vote_set",
                "vote_set__user",
                Prefetch(
                    "vote_set",
                    to_attr="user_vote",
                    queryset=Vote.objects.filter(user=self.request.user),
                ),
            )
        )

    def get_context_data(self, **kwargs):
        # Provide easier access to film in the template
        context = super().get_context_data(**kwargs)
        context["films"] = [film for film in self.object_list if not film.is_watched]
        context["watched_films"] = [
            film for film in self.object_list if film.is_watched
        ]
        context["num_to_watch"] = len(context["films"])
        return context
