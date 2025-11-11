from django.urls import path

from .views import check_guess, create_game, game_detail, guess_history

urlpatterns = [
    path("games/", create_game, name="create-game"),
    path("games/<int:game_id>/guess/", check_guess, name="check-guess"),
    path("games/<int:game_id>/", game_detail, name="game-detail"),
    path("games/<int:game_id>/history/", guess_history, name="guess-history"),
]

