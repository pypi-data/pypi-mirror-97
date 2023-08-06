from django.contrib import admin

from films import models


@admin.register(models.Film)
class RegisterAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = (
        "title",
        "year",
        "age_rating",
        "imdb_age",
        "bbfc_age",
        "is_available",
        "is_watched",
    )
    list_filter = ("is_available", "is_watched", "imdb_age", "bbfc_age", "year")
    view_on_site = True
