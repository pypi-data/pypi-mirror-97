from django.urls import path

from calender import views
from calender.apps import CalenderConfig

app_name = CalenderConfig.name
urlpatterns = [
    path("<int:pk>/", views.RegisterUpdate.as_view(), name="register-update")
]
