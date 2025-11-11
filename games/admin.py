from django.contrib import admin

from .models import Game, GameGuess


class GameGuessInline(admin.TabularInline):
    model = GameGuess
    extra = 0
    readonly_fields = ("guess", "well_placed", "misplaced", "created_at")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "attempts_used", "max_attempts", "is_solved", "created_at")
    search_fields = ("code",)
    ordering = ("-created_at",)
    readonly_fields = ("attempts_used", "created_at")
    inlines = [GameGuessInline]

