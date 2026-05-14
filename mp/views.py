from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .emotion import predict_emotion
from .forms import UploadImageForm
from .models import Prediction


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

            label, confidence, scores = predict_emotion(prediction.image.path)
            prediction.predicted_emotion = label
            prediction.confidence = confidence
            prediction.raw_scores = scores
            prediction.save()

            return redirect("mp:result", pk=prediction.pk)
    else:
        form = UploadImageForm()
    return render(request, "mp/upload.html", {"form": form})


@login_required
def result(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk, user=request.user)
    sorted_scores = sorted(
        prediction.raw_scores.items(), key=lambda kv: kv[1], reverse=True
    )
    return render(
        request,
        "mp/result.html",
        {"prediction": prediction, "sorted_scores": sorted_scores},
    )


@login_required
def history(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, "mp/history.html", {"predictions": predictions})
