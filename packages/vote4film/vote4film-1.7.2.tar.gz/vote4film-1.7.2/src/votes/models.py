from django.conf import settings
from django.db import models
from django.urls import reverse


class Vote(models.Model):
    class Meta:
        unique_together = [["user", "film"]]

    YES = 2
    YES_MAYBE = 1
    NO = -1
    NO_WAY = -2
    VOTE_CHOICES = [
        (YES, "Yes please"),
        (YES_MAYBE, "Yes - if I must"),
        (NO, "No thanks"),
        (NO_WAY, "No - definitely not"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey("films.Film", on_delete=models.CASCADE)
    choice = models.IntegerField(choices=VOTE_CHOICES)

    def get_absolute_url(self):
        return reverse("votes:vote-update", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Vote by {self.user} of {self.choice} for {self.film}"

    def __repr__(self):
        return f"<Vote(pk={self.pk})>"
