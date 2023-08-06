from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse


class EventQuerySet(models.QuerySet):
    def future_events(self):
        # TODO: This might not be right even for Europe/London!
        today = datetime.utcnow().date()
        return self.filter(date__gte=today).order_by("date")


class Event(models.Model):
    date = models.DateField(unique=True)

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return f"Event on {self.date}"

    def __repr__(self):
        return f"<Event(pk={self.pk})>"


class RegisterQuerySet(models.QuerySet):
    def has_registered(self, user):
        next_event = Event.objects.future_events().first()
        if not next_event:
            return False

        register = Register.objects.filter(user=user, event=next_event).first()
        if not register:
            return False

        return register.is_registered

    def next_event_register(self, user):
        next_event = Event.objects.future_events().first()
        if not next_event:
            return Register.objects.none()

        return Register.objects.get_or_create(user=user, event=next_event)[0]

    def present_for(self, event):
        return self.filter(event=event, is_present=True).select_related("user")

    def absent_for(self, event):
        return self.filter(event=event, is_present=False).select_related("user")

    def unknown_for(self, event):
        raise NotImplementedError("# TODO: Create Register objects")


class Register(models.Model):
    class Meta:
        unique_together = [["user", "event"]]

    objects = RegisterQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_present = models.NullBooleanField()

    @property
    def is_registered(self):
        return self.is_present is not None

    def get_absolute_url(self):
        return reverse("calender:register-update", kwargs={"pk": self.pk})

    def __str__(self):
        mapping = {
            None: "an unknown",
            True: "present",
            False: "absent",
        }
        state = mapping[self.is_present]
        return f"{self.user} is {state} on {self.event.date}"

    def __repr__(self):
        return f"<Register(pk={self.pk})>"
