import base64
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .emotion import predict_emotion
from .forms import UploadImageForm
from .journey import caption_for, embed_for, get_journey, DEFAULT_PHASE_SONG_COUNT
from .models import Prediction, Song


def home(request):
    return render(request, "mp/home.html")


@login_required
def upload(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.user = request.user
            prediction.save()
            _run_prediction(prediction)
            return redirect("mp:result", pk=prediction.pk)
    else:
        form = UploadImageForm()
    return render(request, "mp/upload.html", {"form": form})


@login_required
def live(request):
    """Live webcam mood-detection page."""
    return render(request, "mp/live.html")


@login_required
@require_POST
@csrf_protect
def api_predict_frame(request):
    """Accept a base64-encoded webcam frame and return mood + playlist URL.

    Body: JSON or form-data with field `image_data` containing a data: URL
    (image/jpeg or image/png).
    """
    data_url = request.POST.get("image_data", "")
    if not data_url.startswith("data:image"):
        return JsonResponse({"error": "image_data must be a data: URL"}, status=400)
    try:
        _, b64 = data_url.split(",", 1)
        raw = base64.b64decode(b64)
    except Exception:
        return JsonResponse({"error": "invalid image data"}, status=400)

    prediction = Prediction(user=request.user)
    prediction.image.save(
        f"webcam_{request.user.id}.jpg", ContentFile(raw), save=False
    )
    prediction.save()
    _run_prediction(prediction)

    return JsonResponse({
        "mood": prediction.predicted_emotion,
        "confidence": prediction.confidence,
        "scores": prediction.raw_scores,
        "result_url": reverse("mp:result", args=[prediction.pk]),
    })


@login_required
def result(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk, user=request.user)
    sorted_scores = sorted(
        prediction.raw_scores.items(), key=lambda kv: kv[1], reverse=True
    )

    phases = get_journey(prediction.predicted_emotion)
    journey_playlist = []
    for phase in phases:
        songs = list(Song.objects.filter(mood=phase).order_by("?")[:DEFAULT_PHASE_SONG_COUNT])
        for song in songs:
            journey_playlist.append({
                "song": song,
                "phase": phase,
                "phase_caption": caption_for(phase),
                "embed_url": embed_for(song),
            })

    return render(
        request,
        "mp/result.html",
        {
            "prediction": prediction,
            "sorted_scores": sorted_scores,
            "journey_playlist": journey_playlist,
            "phases": [{"key": p, "caption": caption_for(p)} for p in phases],
        },
    )


@login_required
def history(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, "mp/history.html", {"predictions": predictions})


def library(request):
    songs_by_mood = {
        mood: Song.objects.filter(mood=mood)
        for mood, _ in __import__("mp.models", fromlist=["MOOD_CHOICES"]).MOOD_CHOICES
    }
    return render(request, "mp/library.html", {"songs_by_mood": songs_by_mood})


def _run_prediction(prediction: Prediction) -> None:
    label, confidence, scores = predict_emotion(prediction.image.path)
    prediction.predicted_emotion = label
    prediction.confidence = confidence
    prediction.raw_scores = scores
    prediction.save()
