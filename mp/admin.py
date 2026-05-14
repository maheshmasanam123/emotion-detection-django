from django.contrib import admin

from .models import Prediction, Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "mood", "source", "uploaded_at")
    list_filter = ("mood", "source")
    search_fields = ("title", "artist")
    fieldsets = (
        ("Track info", {"fields": ("title", "artist", "mood", "cover")}),
        ("Audio source", {
            "fields": ("audio", "external_url", "source"),
            "description": "Upload a file OR paste an external URL "
                           "(YouTube / Spotify / SoundCloud).",
        }),
    )
    readonly_fields = ("source",)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "predicted_emotion", "confidence", "created_at")
    list_filter = ("predicted_emotion", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
