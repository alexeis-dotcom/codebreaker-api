from collections.abc import Callable
from typing import Any

import pytest
from rest_framework.test import APIClient

from games.models import Game, GameGuess


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def game_factory(db) -> Callable[..., Game]:
    """Factory fixture for creating Game instances with custom attributes."""
    def _factory(**kwargs: Any) -> Game:
        defaults = {"code": "1234"}
        defaults.update(kwargs)
        return Game.objects.create(**defaults)

    return _factory


@pytest.fixture
def game_guess_factory(db) -> Callable[..., GameGuess]:
    """Factory fixture for creating GameGuess instances with custom attributes."""
    def _factory(game: Game, **kwargs: Any) -> GameGuess:
        defaults = {
            "guess": "1234",
            "well_placed": 0,
            "misplaced": 0,
        }
        defaults.update(kwargs)
        return GameGuess.objects.create(game=game, **defaults)

    return _factory


@pytest.fixture
def sample_game(game_factory) -> Game:
    """Provides a standard game instance for tests."""
    return game_factory(code="1234", attempts_used=0, max_attempts=10)
