from __future__ import annotations

from typing import Iterable, TypedDict


class GuessEvaluation(TypedDict):
    well_placed: int
    misplaced: int


def evaluate_guess(guess: Iterable[int], secret: Iterable[int]) -> GuessEvaluation:
    """
    Compare a 4-digit guess against the secret code and return counts of well placed and misplaced digits.
    """
    guess_list = list(guess)
    secret_list = list(secret)

    if len(guess_list) != len(secret_list):
        raise ValueError("Guess and secret must be the same length.")

    guess_copy: list[int] = guess_list[:]
    secret_copy: list[int] = secret_list[:]

    well_placed = 0
    misplaced = 0

    for index in range(len(secret_copy)):
        if secret_copy[index] == guess_copy[index]:
            well_placed += 1
            secret_copy[index] = -1
            guess_copy[index] = -1

    for index in range(len(secret_copy)):
        if guess_copy[index] != -1:
            try:
                misplaced_index = secret_copy.index(guess_copy[index])
            except ValueError:
                continue
            misplaced += 1
            secret_copy[misplaced_index] = -1

    return {"well_placed": well_placed, "misplaced": misplaced}

