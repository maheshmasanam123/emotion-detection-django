from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from .forms import SignupForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("mp:home")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


class AppLoginView(LoginView):
    template_name = "accounts/login.html"


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
