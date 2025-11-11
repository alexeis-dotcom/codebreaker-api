from __future__ import annotations

from rest_framework import serializers

from .models import FOUR_DIGIT_VALIDATOR, Game, GameGuess


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
    )


class GameSerializer(serializers.ModelSerializer):
    remaining_attempts = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = (
            "id",
            "attempts_used",
            "max_attempts",
            "remaining_attempts",
            "is_solved",
            "created_at",
        )
        read_only_fields = fields

    def get_remaining_attempts(self, obj: Game) -> int:
        return obj.remaining_attempts


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGuess
        fields = ("id", "game_id", "guess", "well_placed", "misplaced", "created_at")
        read_only_fields = fields


class GuessResponseSerializer(serializers.Serializer):
    game = GameSerializer()
    guess = GuessSerializer()


class GuessHistoryResponseSerializer(serializers.Serializer):
    game = GameSerializer()
    history = GuessSerializer(many=True)

