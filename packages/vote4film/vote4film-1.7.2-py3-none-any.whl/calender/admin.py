from django.contrib import admin

from calender import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("date",)
    list_filter = ("date",)


@admin.register(models.Register)
class RegisterAdmin(admin.ModelAdmin):
    date_hierarchy = "event__date"
    list_display = ("__str__", "user", "event", "is_present")
    list_filter = ("is_present", "user", "event__date")
    readonly_fields = ("user", "event")
    fields = ("user", "event", "is_present")
