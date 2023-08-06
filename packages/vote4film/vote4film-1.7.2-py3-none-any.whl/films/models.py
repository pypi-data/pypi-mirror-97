import urllib.parse

from django.db import models
from django.urls import reverse


class FilmQuerySet(models.QuerySet):
    def potentially_watchable(self):
        return self.filter(is_watched=False, is_available=True)


class Film(models.Model):
    class Meta:
        unique_together = [["title", "year"]]

    UNIVERSAL = "U"
    PARENTAL_GUIDANCE = "PG"
    AGE_12 = "12"  # Including 12A
    AGE_15 = "15"
    AGE_18 = "18"  # Including R18
    AGE_RATING_CHOICES = [
        (UNIVERSAL, "Universal (4+)"),
        (PARENTAL_GUIDANCE, "Parental Guidance (8+)"),
        (AGE_12, "12+"),
        (AGE_15, "15+"),
        (AGE_18, "18+"),
    ]

    objects = FilmQuerySet.as_manager()

    imdb = models.URLField(verbose_name="IMDB Link")
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(verbose_name="Year of Release")
    imdb_age = models.CharField(
        verbose_name="IMDB Age Rating",
        null=True,
        blank=True,
        max_length=3,
        choices=AGE_RATING_CHOICES,
    )
    bbfc_age = models.CharField(
        verbose_name="BBFC Age Rating",
        null=True,
        blank=True,
        max_length=3,
        choices=AGE_RATING_CHOICES,
    )
    imdb_rating = models.FloatField(verbose_name="IMDB Rating")
    trailer = models.URLField(verbose_name="Trailer Link", null=True, blank=True)
    genre = models.CharField(null=True, blank=True, max_length=255)
    runtime_mins = models.PositiveIntegerField(
        verbose_name="Runtime (minutes)", null=True, blank=True
    )
    plot = models.TextField(null=True, blank=True)
    poster_url = models.URLField(verbose_name="Poster URL", null=True, blank=True)
    is_available = models.BooleanField(verbose_name="Do we have it?", default=False)
    is_watched = models.BooleanField(verbose_name="Have we watched it?", default=False)

    @property
    def bbfc_search(self):
        query_string = urllib.parse.urlencode(
            {
                "q": self.title,
                "s": "Newest",
                "t[]": "Film",
            }
        )
        return f"https://www.bbfc.co.uk/search?{query_string}"

    @property
    def youtube_search(self):
        query_string = urllib.parse.urlencode(
            {"search_query": f"{self.title} {self.year} Trailer"}
        )
        return f"https://www.youtube.com/results?{query_string}"

    @property
    def age_rating(self):
        return self.bbfc_age or self.imdb_age

    def get_absolute_url(self):
        return reverse("films:film-update", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title} ({self.year})"

    def __repr__(self):
        return f"<Film(pk={self.pk})>"
