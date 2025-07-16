# core/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from curriculum.models import Grade

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "core/register.html", {"form": form})

def dashboard_view(request):
    grades = Grade.objects.all()  # fetch grades
    return render(request, "core/dashboard.html", {"grades": grades})
def home_view(request):
    return render(request, "core/home.html")

def grades_view(request, grade_number):
    return render(request, "grade_detail.html", {"grade_number": grade_number})