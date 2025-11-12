from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .exceptions import (
    GameAlreadySolved,
    GameMaxAttemptsReached,
)
from .models import CODE_LENGTH, Game, GameGuess
from .serializers import (
    GameSerializer,
    GuessHistoryResponseSerializer,
    GuessInputSerializer,
    GuessResponseSerializer,
)
from .services import evaluate_guess


class GameViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Game.objects.all()
    lookup_field = "pk"
    serializer_class = GameSerializer

    def get_queryset(self):
        if getattr(self, "action", None) == "history":
            return Game.objects.prefetch_related("guesses")
        return super().get_queryset()

    def get_serializer_class(self):
        if getattr(self, "action", None) == "guess":
            return GuessInputSerializer
        if getattr(self, "action", None) == "history":
            return GuessHistoryResponseSerializer
        return GameSerializer

    @extend_schema(tags=["Games"], request=GameSerializer, responses=GameSerializer)
    def create(self, request, *args, **kwargs) -> Response:
        serializer = GameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Games"], responses=GameSerializer)
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Games"],
        request=GuessInputSerializer,
        responses=GuessResponseSerializer,
    )
    @action(detail=True, methods=["post"], url_path="guess", serializer_class=GuessInputSerializer)
    def guess(self, request, *args, **kwargs) -> Response:
        serializer = GuessInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        guess_value = serializer.validated_data["guess"]

        with transaction.atomic():
            game = Game.objects.select_for_update().get(pk=self.kwargs[self.lookup_field])

            if game.is_solved:
                raise GameAlreadySolved()

            if game.attempts_used >= game.max_attempts:
                raise GameMaxAttemptsReached()

            guess_digits = [int(char) for char in guess_value]
            secret_digits = [int(char) for char in game.code]
            evaluation = evaluate_guess(guess_digits, secret_digits)

            guess = GameGuess.objects.create(
                game=game,
                guess=guess_value,
                well_placed=evaluation["well_placed"],
                misplaced=evaluation["misplaced"],
            )

            game.attempts_used += 1
            if evaluation["well_placed"] == CODE_LENGTH:
                game.is_solved = True
            game.save(update_fields=["attempts_used", "is_solved"])

        response_serializer = GuessResponseSerializer({"game": game, "guess": guess})
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["Games"], responses=GuessHistoryResponseSerializer)
    @action(detail=True, methods=["get"], url_path="history", serializer_class=GuessHistoryResponseSerializer)
    def history(self, request, *args, **kwargs) -> Response:
        game = self.get_object()
        serializer = GuessHistoryResponseSerializer({"game": game, "history": list(game.guesses.all())})
        return Response(serializer.data, status=status.HTTP_200_OK)
