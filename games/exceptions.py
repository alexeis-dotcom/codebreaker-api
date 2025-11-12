from rest_framework import status
from rest_framework.exceptions import APIException


class GameAlreadySolved(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Game is already solved."
    default_code = "game_already_solved"


class GameMaxAttemptsReached(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Maximum number of attempts reached."
    default_code = "game_max_attempts_reached"
