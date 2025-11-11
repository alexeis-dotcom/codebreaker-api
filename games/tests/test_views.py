from __future__ import annotations

from rest_framework import status
from rest_framework.test import APITestCase

from games.models import Game, GameGuess


class GameAPITests(APITestCase):
    def test_create_game_success(self) -> None:
        response = self.client.post("/api/games/", {"code": "1234"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("game", response.data)
        self.assertEqual(response.data["game"]["attempts_used"], 0)
        self.assertTrue(Game.objects.filter(code="1234").exists())

    def test_create_game_invalid_code(self) -> None:
        response = self.client.post("/api/games/", {"code": "12a4"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("code", response.data)
        self.assertIn("Value must be exactly 4 digits.", response.data["code"][0])

    def test_check_guess_updates_game_and_returns_evaluation(self) -> None:
        game = Game.objects.create(code="1234")

        response = self.client.post(
            f"/api/games/{game.id}/guess/",
            {"code": "1256"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["guess"]["well_placed"], 2)
        self.assertEqual(data["guess"]["misplaced"], 0)

        game.refresh_from_db()
        self.assertEqual(game.attempts_used, 1)
        self.assertFalse(game.is_solved)
        self.assertTrue(GameGuess.objects.filter(game=game, guess="1256").exists())

    def test_check_guess_conflict_when_game_solved(self) -> None:
        game = Game.objects.create(code="1234", is_solved=True)

        response = self.client.post(
            f"/api/games/{game.id}/guess/",
            {"code": "1234"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("error", response.data)

    def test_check_guess_conflict_when_attempts_exhausted(self) -> None:
        game = Game.objects.create(code="1234", attempts_used=10, max_attempts=10)

        response = self.client.post(
            f"/api/games/{game.id}/guess/",
            {"code": "1234"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("error", response.data)

    def test_guess_history_returns_guesses(self) -> None:
        game = Game.objects.create(code="1234")
        GameGuess.objects.create(game=game, guess="1234", well_placed=4, misplaced=0)
        GameGuess.objects.create(game=game, guess="4321", well_placed=0, misplaced=4)

        response = self.client.get(f"/api/games/{game.id}/history/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        history = response.data["history"]
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["guess"], "1234")
        self.assertEqual(history[1]["guess"], "4321")

    def test_game_detail_returns_game_metadata(self) -> None:
        game = Game.objects.create(code="9876", attempts_used=3, max_attempts=10)

        response = self.client.get(f"/api/games/{game.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data["game"]
        self.assertEqual(payload["id"], game.id)
        self.assertEqual(payload["attempts_used"], 3)
        self.assertEqual(payload["remaining_attempts"], 7)

