from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

FOUR_DIGIT_VALIDATOR = RegexValidator(regex=r"^\d{4}$", message="Value must be exactly 4 digits.")


class Game(models.Model):
    code = models.CharField(
        max_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
    )
    attempts_used = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=10)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Game #{self.pk} ({self.code})"

    @property
    def remaining_attempts(self) -> int:
        return max(self.max_attempts - self.attempts_used, 0)

class GameGuess(models.Model):
    game = models.ForeignKey(Game, related_name="guesses", on_delete=models.CASCADE)
    guess = models.CharField(
        max_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
    )
    well_placed = models.PositiveSmallIntegerField()
    misplaced = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Guess {self.guess} for Game #{self.game_id}"

