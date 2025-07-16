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

def home_view(request):
    return render(request, "core/home.html")

def grades_view(request, grade_id):
    #show based on grade_id
    if grade_id.upper() == "SHSAT":
        page_title = "SHSAT Math Prep"
        description = "Specialized lessons and practice for the SHSAT exam."
    elif grade_id.upper() == "SAT":
        page_title = "SAT Math Prep"
        description = "Focused math prep for the SAT exam."
    else:
        page_title = f"Grade {grade_id} Math"
        description = f"Lessons and practice for Grade {grade_id} students."

    return render(request, "core/grade_detail.html", {
        "grade_id": grade_id,
        "page_title": page_title,
        "description": description
    })