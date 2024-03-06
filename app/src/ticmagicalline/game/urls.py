from django.urls import path
import pretty_errors
from . import views

urlpatterns = [
    path("", views.indexView, name="index"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("game/create", views.createGameView, name="create"),
    path("game/play/<int:id>", views.playGameView, name="play"),
]
