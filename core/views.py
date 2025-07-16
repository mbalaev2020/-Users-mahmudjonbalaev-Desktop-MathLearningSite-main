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
    # Map SHSAT & SAT to numeric levels
    if grade_id.upper() == "SHSAT":
        level = 9
    elif grade_id.upper() == "SAT":
        level = 10
    else:
        level = int(grade_id)

    # Fetch Grade & prefetch Domains→Standards
    grade = Grade.objects.prefetch_related("domains__standards").filter(level=level).first()

    # Handle missing grade gracefully
    if not grade:
        return render(request, "core/grade_detail.html", {
            "page_title": "Not Found",
            "description": "No data available for this grade.",
            "grade": None,
        })

    # Title auto-converts 9→SHSAT, 10→SAT via Grade.__str__()
    page_title = str(grade)
    description = f"Explore domains and standards for {grade}."

    return render(request, "core/grade_detail.html", {
        "grade": grade,  # we now pass the full grade object
        "page_title": page_title,
        "description": description,
    })