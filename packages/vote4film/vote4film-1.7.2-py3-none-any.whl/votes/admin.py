from django.contrib import admin

from votes import models


@admin.register(models.Vote)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "film", "choice")
    list_filter = ("choice", "user", "film")
    readonly_fields = ("user", "film")
    fields = ("user", "film", "choice")
