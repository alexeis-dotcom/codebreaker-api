import json

from django.db import DatabaseError, transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import CodeForm
from .models import Game, GameGuess
from .serializers import serialize_game, serialize_guess, serialize_guess_history
from .services import evaluate_guess


def _validate_code(payload: dict[str, object]) -> tuple[str, JsonResponse | None]:
    form = CodeForm(payload)
    if not form.is_valid():
        errors = form.errors.get("code")
        message = errors[0] if errors else "Invalid code."
        return "", JsonResponse({"error": message}, status=400)
    return form.cleaned_data["code"], None


@csrf_exempt
@require_http_methods(["POST"])
def create_game(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    code, error_response = _validate_code(payload)
    if error_response is not None:
        return error_response

    try:
        game = Game.objects.create(code=code)
    except DatabaseError:
        return JsonResponse({"error": "Failed to create game due to database error."}, status=500)

    return JsonResponse({"id": game.id}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def check_guess(request: HttpRequest, game_id: int) -> JsonResponse:
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    code_value, error_response = _validate_code(payload)
    if error_response is not None:
        return error_response

    with transaction.atomic():
        try:
            game = Game.objects.select_for_update().get(pk=game_id)
        except Game.DoesNotExist:
            return JsonResponse({"error": "Game not found."}, status=404)

        if game.is_solved:
            return JsonResponse({"error": "Game is already solved."}, status=409)

        if game.attempts_used >= game.max_attempts:
            return JsonResponse({"error": "Maximum number of attempts reached."}, status=409)

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

    response_payload = {"game": serialize_game(game), "guess": serialize_guess(guess)}

    return JsonResponse(response_payload, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def guess_history(request: HttpRequest, game_id: int) -> JsonResponse:
    try:
        game = Game.objects.prefetch_related("guesses").get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found."}, status=404)

    guesses = game.guesses.all()
    response_payload = {"game": serialize_game(game), "history": serialize_guess_history(guesses)}

    return JsonResponse(response_payload, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def game_detail(request: HttpRequest, game_id: int) -> JsonResponse:
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found."}, status=404)

    response_payload = serialize_game(game)

    return JsonResponse(response_payload, status=200)

