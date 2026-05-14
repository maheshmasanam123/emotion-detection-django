from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

MOOD_CHOICES = [
    ("angry", "Angry"),
    ("calm", "Calm"),
    ("chill", "Chill"),
    ("sad", "Sad"),
    ("motivation", "Motivation"),
    ("uplift", "Uplifting"),
    ("happy", "Happy"),
    ("neutral", "Neutral"),
    ("party", "Party"),
]

SOURCE_CHOICES = [
    ("local", "Local file"),
    ("youtube", "YouTube"),
    ("spotify", "Spotify"),
    ("soundcloud", "SoundCloud"),
    ("other", "Other link"),
]


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True)
    mood = models.CharField(max_length=16, choices=MOOD_CHOICES, db_index=True)

    audio = models.FileField(
        upload_to="songs/", blank=True, null=True,
        help_text="Upload an MP3/OGG/WAV. Leave empty if using an external link.",
    )
    external_url = models.URLField(
        blank=True,
        help_text="Paste a YouTube, Spotify, or SoundCloud link as an alternative to uploading.",
    )
    source = models.CharField(
        max_length=16, choices=SOURCE_CHOICES, default="local",
        help_text="Auto-detected on save if external_url is set.",
    )

    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["mood", "title"]

    def __str__(self):
        return f"{self.title} ({self.mood})"

    def clean(self):
        if not self.audio and not self.external_url:
            raise ValidationError("Provide either an audio file or an external URL.")

    def save(self, *args, **kwargs):
        if self.external_url and self.source == "local":
            url = self.external_url.lower()
            if "youtube.com" in url or "youtu.be" in url:
                self.source = "youtube"
            elif "spotify.com" in url:
                self.source = "spotify"
            elif "soundcloud.com" in url:
                self.source = "soundcloud"
            else:
                self.source = "other"
        super().save(*args, **kwargs)


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
