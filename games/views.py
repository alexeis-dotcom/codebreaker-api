import json

from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Game


@csrf_exempt
@require_http_methods(["POST"])
def create_game(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    code = payload.get("code")
    if code is None:
        return JsonResponse({"error": "Field 'code' is required."}, status=400)

    if not isinstance(code, str) or not code.isdigit() or len(code) != 4:
        return JsonResponse({"error": "Code must be a 4-digit string."}, status=400)

    try:
        game = Game.objects.create(code=code)
    except Exception:
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"id": game.id}, status=201)

