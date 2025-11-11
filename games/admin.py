from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "created_at")
    search_fields = ("code",)
    ordering = ("-created_at",)

