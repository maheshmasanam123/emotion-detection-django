from django.conf import settings
from django.db import models


class Prediction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    predicted_emotion = models.CharField(max_length=32)
    confidence = models.FloatField(default=0.0)
    raw_scores = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.predicted_emotion} ({self.confidence:.2f}) @ {self.created_at:%Y-%m-%d %H:%M}"
