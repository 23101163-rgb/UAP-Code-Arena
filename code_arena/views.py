from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Sum, Max
from datetime import timedelta
from .forms import UserSignupForm, UserLoginForm
from .models import  User,Submission,Contest,Problem
from django.contrib.auth.forms import AuthenticationForm
def signup_view(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserSignupForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    # If the user is already logged in, render the login page again
    if request.user.is_authenticated:
        return render(request, "login.html", {"form": AuthenticationForm()})

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # After successful login, do not redirect to home for now
            return render(request, "login.html", {"form": AuthenticationForm()})  # Just render the login page
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
def home_view(request):
    # Top 5 users (by points)
    top_users = User.objects.filter(is_staff=False).order_by('-points')[:8]

    # Active contests (currently running)
    now = timezone.now()
    upcoming_contests = Contest.objects.filter(start_time__gt=now).order_by('start_time')[:3]
    recent_submissions = Submission.objects.filter(user=request.user).order_by('-created_at')[:3]

    context = {
        'top_users': top_users,
        "upcoming_contests": upcoming_contests,
        'recent_submissions': recent_submissions,
    }
    return render(request, "home.html", context)

User = get_user_model()