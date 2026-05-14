from django.urls import path

from . import views

app_name = "mp"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload, name="upload"),
    path("live/", views.live, name="live"),
    path("api/predict-frame/", views.api_predict_frame, name="api_predict_frame"),
    path("result/<int:pk>/", views.result, name="result"),
    path("history/", views.history, name="history"),
    path("library/", views.library, name="library"),
]
