from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import path
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "web/home.html"


class LoginView(LoginView):
    template_name = "web/login.html"


safe_logout_then_login = require_POST(logout_then_login)

app_name = "web"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("logout/", safe_logout_then_login, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
]
