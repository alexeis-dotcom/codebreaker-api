from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Game(models.Model):
    code = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex=r"^\d{4}$", message="Code must be exactly 4 digits.")],
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Game #{self.pk} ({self.code})"

