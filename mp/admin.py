from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "predicted_emotion", "confidence", "created_at")
    list_filter = ("predicted_emotion", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
