from typing import Mapping

from django.db import DatabaseError, transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Game, GameGuess
from .serializers import (
    CodeSerializer,
    GameResponseSerializer,
    GuessHistoryResponseSerializer,
    GuessResponseSerializer,
    GuessSerializer,
)
from .services import evaluate_guess


def _validate_code(data: Mapping[str, object]) -> str:
    serializer = CodeSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data["code"]

@extend_schema(request=CodeSerializer, responses=GameResponseSerializer)
@api_view(["POST"])
def create_game(request) -> Response:
    code = _validate_code(request.data)

    try:
        game = Game.objects.create(code=code)
    except DatabaseError:
        return Response(
            {"error": "Failed to create game due to database error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response_serializer = GameResponseSerializer({"game": game})
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(request=CodeSerializer, responses=GuessResponseSerializer)
@api_view(["POST"])
def check_guess(request, game_id: int) -> Response:
    code_value = _validate_code(request.data)

    with transaction.atomic():
        game = get_object_or_404(Game.objects.select_for_update(), pk=game_id)

        if game.is_solved:
            return Response(
                {"error": "Game is already solved."},
                status=status.HTTP_409_CONFLICT,
            )

        if game.attempts_used >= game.max_attempts:
            return Response(
                {"error": "Maximum number of attempts reached."},
                status=status.HTTP_409_CONFLICT,
            )

        guess_digits = [int(char) for char in code_value]
        secret_digits = [int(char) for char in game.code]
        evaluation = evaluate_guess(guess_digits, secret_digits)

        guess = GameGuess.objects.create(
            game=game,
            guess=code_value,
            well_placed=evaluation["well_placed"],
            misplaced=evaluation["misplaced"],
        )

        game.attempts_used += 1
        if evaluation["well_placed"] == 4:
            game.is_solved = True
        game.save(update_fields=["attempts_used", "is_solved"])

    response_serializer = GuessResponseSerializer({"game": game, "guess": guess})
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(responses=GuessHistoryResponseSerializer)
@api_view(["GET"])
def guess_history(request, game_id: int) -> Response:
    game = get_object_or_404(Game.objects.prefetch_related("guesses"), pk=game_id)
    response_serializer = GuessHistoryResponseSerializer(
        {
            "game": game,
            "history": list(game.guesses.all()),
        }
    )
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(responses=GameResponseSerializer)
@api_view(["GET"])
def game_detail(request, game_id: int) -> Response:
    game = get_object_or_404(Game, pk=game_id)
    serializer = GameResponseSerializer({"game": game})
    return Response(serializer.data, status=status.HTTP_200_OK)

