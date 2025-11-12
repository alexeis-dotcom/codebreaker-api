from __future__ import annotations

from rest_framework import serializers

from .models import FOUR_DIGIT_VALIDATOR, Game, GameGuess


class GameSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
    )
    remaining_attempts = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = (
            "id",
            "code",
            "attempts_used",
            "max_attempts",
            "remaining_attempts",
            "is_solved",
            "created_at",
        )
        read_only_fields = (
            "id",
            "attempts_used",
            "max_attempts",
            "remaining_attempts",
            "is_solved",
            "created_at",
        )

    def get_remaining_attempts(self, obj: Game) -> int:
        return obj.remaining_attempts


class GuessSerializer(serializers.ModelSerializer):
    guess = serializers.CharField(
        max_length=4,
        min_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
    )

    class Meta:
        model = GameGuess
        fields = ("id", "game_id", "guess", "well_placed", "misplaced", "created_at")
        read_only_fields = ("id", "game_id", "well_placed", "misplaced", "created_at")


class GuessInputSerializer(serializers.Serializer):
    guess = serializers.CharField(
        max_length=4,
        min_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
    )


class GuessResponseSerializer(serializers.Serializer):
    game = GameSerializer()
    guess = GuessSerializer()


class GuessHistoryResponseSerializer(serializers.Serializer):
    game = GameSerializer()
    history = GuessSerializer(many=True)
