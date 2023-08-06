from django.urls import path

from votes import views
from votes.apps import VotesConfig

app_name = VotesConfig.name
urlpatterns = [
    path("create/", views.VoteCreate.as_view(), name="vote-create"),
    path("<int:pk>/", views.VoteUpdate.as_view(), name="vote-update"),
    path("", views.VoteAggregate.as_view(), name="vote-aggregate"),
]
