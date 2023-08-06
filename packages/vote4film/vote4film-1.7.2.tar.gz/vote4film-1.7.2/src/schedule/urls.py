from django.urls import path

from schedule import views
from schedule.apps import ScheduleConfig

app_name = ScheduleConfig.name
urlpatterns = [path("", views.Schedule.as_view(), name="schedule")]
