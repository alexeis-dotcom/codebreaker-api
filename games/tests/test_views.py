import pytest
from rest_framework import status

from games.models import Game, GameGuess


@pytest.mark.django_db
def test_create_game_success(api_client) -> None:
    response = api_client.post("/api/games/", {"code": "1234"}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["code"] == "1234"
    assert response.data["attempts_used"] == 0
    assert Game.objects.filter(code="1234").exists()


@pytest.mark.django_db
def test_create_game_invalid_code(api_client) -> None:
    response = api_client.post("/api/games/", {"code": "12a4"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "code" in response.data
    assert "Value must be exactly 4 digits." in response.data["code"][0]


@pytest.mark.django_db
def test_check_guess_updates_game_and_returns_evaluation(api_client, game_factory) -> None:
    game = game_factory(code="1234")

    response = api_client.post(
        f"/api/games/{game.id}/guess/",
        {"guess": "1256"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data["game"]["code"] == "1234"
    assert data["guess"]["well_placed"] == 2
    assert data["guess"]["misplaced"] == 0

    game.refresh_from_db()
    assert game.attempts_used == 1
    assert not game.is_solved
    assert GameGuess.objects.filter(game=game, guess="1256").exists()


@pytest.mark.django_db
def test_check_guess_conflict_when_game_solved(api_client, game_factory) -> None:
    game = game_factory(code="1234", is_solved=True)

    response = api_client.post(
        f"/api/games/{game.id}/guess/",
        {"guess": "1234"},
        format="json",
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data["detail"] == "Game is already solved."


@pytest.mark.django_db
def test_check_guess_conflict_when_attempts_exhausted(api_client, game_factory) -> None:
    game = game_factory(code="1234", attempts_used=10, max_attempts=10)

    response = api_client.post(
        f"/api/games/{game.id}/guess/",
        {"guess": "1234"},
        format="json",
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data["detail"] == "Maximum number of attempts reached."


@pytest.mark.django_db
def test_guess_history_returns_guesses(api_client, game_factory, game_guess_factory) -> None:
    game = game_factory(code="1234")
    game_guess_factory(game=game, guess="1234", well_placed=4, misplaced=0)
    game_guess_factory(game=game, guess="4321", well_placed=0, misplaced=4)

    response = api_client.get(f"/api/games/{game.id}/history/")

    assert response.status_code == status.HTTP_200_OK
    history = response.data["history"]
    assert response.data["game"]["code"] == "1234"
    assert len(history) == 2
    assert history[0]["guess"] == "1234"
    assert history[1]["guess"] == "4321"


@pytest.mark.django_db
def test_game_detail_returns_game_metadata(api_client, game_factory) -> None:
    game = game_factory(code="9876", attempts_used=3, max_attempts=10)

    response = api_client.get(f"/api/games/{game.id}/")

    assert response.status_code == status.HTTP_200_OK
    payload = response.data
    assert payload["id"] == game.id
    assert payload["code"] == "9876"
    assert payload["attempts_used"] == 3
    assert payload["remaining_attempts"] == 7
