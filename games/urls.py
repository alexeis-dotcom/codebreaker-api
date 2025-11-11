from django.urls import path

from .views import create_game

urlpatterns = [
    path("games/", create_game, name="create-game"),
]

