from django.contrib import admin

from .models import Prediction, Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "mood", "uploaded_at")
    list_filter = ("mood",)
    search_fields = ("title", "artist")


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "predicted_emotion", "confidence", "created_at")
    list_filter = ("predicted_emotion", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
