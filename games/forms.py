from __future__ import annotations

from django import forms

from .models import FOUR_DIGIT_VALIDATOR


class CodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        min_length=4,
        validators=[FOUR_DIGIT_VALIDATOR],
        error_messages={
            "required": "Field 'code' is required.",
            "min_length": "Field 'code' must be a 4-digit string.",
            "max_length": "Field 'code' must be a 4-digit string.",
        },
    )

