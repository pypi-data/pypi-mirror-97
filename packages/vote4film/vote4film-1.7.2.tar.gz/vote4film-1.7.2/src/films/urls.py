from django.urls import path

from films import views
from films.apps import FilmConfig

app_name = FilmConfig.name
urlpatterns = [
    path("create/", views.FilmCreate.as_view(), name="film-create"),
    path("<int:pk>/", views.FilmUpdate.as_view(), name="film-update"),
    path("<int:pk>/refresh", views.FilmRefresh.as_view(), name="film-refresh"),
]
