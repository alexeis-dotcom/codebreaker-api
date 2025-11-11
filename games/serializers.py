from __future__ import annotations

from typing import Iterable, TypedDict

from .models import Game, GameGuess


class GamePayload(TypedDict):
    id: int
    attempts_used: int
    max_attempts: int
    remaining_attempts: int
    is_solved: bool
    created_at: str


class GuessPayload(TypedDict):
    id: int
    game_id: int
    guess: str
    well_placed: int
    misplaced: int
    created_at: str


def serialize_game(game: Game) -> GamePayload:
    return {
        "id": game.id,
        "attempts_used": game.attempts_used,
        "max_attempts": game.max_attempts,
        "remaining_attempts": game.remaining_attempts,
        "is_solved": game.is_solved,
        "created_at": game.created_at.isoformat(),
    }


def serialize_guess(guess: GameGuess) -> GuessPayload:
    return {
        "id": guess.id,
        "game_id": guess.game_id,
        "guess": guess.guess,
        "well_placed": guess.well_placed,
        "misplaced": guess.misplaced,
        "created_at": guess.created_at.isoformat(),
    }


def serialize_guess_history(guesses: Iterable[GameGuess]) -> list[GuessPayload]:
    return [serialize_guess(guess) for guess in guesses]

