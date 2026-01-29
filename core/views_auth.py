from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm
from .models import User, ParentLink

@require_http_methods(["GET", "POST"])
def register_student(request):
    form = StudentSignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("portals:student")
    return render(request, "portals/register_student.html", {"form": form})

@require_http_methods(["GET", "POST"])
def register_teacher(request):
    form = TeacherSignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("portals:teacher")
    return render(request, "portals/register_teacher.html", {"form": form})

@require_http_methods(["GET", "POST"])
def register_parent(request):
    form = ParentSignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("core:link_child")
    return render(request, "portals/register_parent.html", {"form": form})

@login_required
@require_http_methods(["GET", "POST"])
def link_child(request):
    """Simple parent→student linking by username."""
    if request.user.role != "parent":
        return redirect("portals:student")

    if request.method == "POST":
        username = request.POST.get("student_username", "").strip()
        relationship = request.POST.get("relationship", "").strip()
        student = User.objects.filter(username=username, role="student").first()
        if not student:
            messages.error(request, "No student found with that username.")
        else:
            ParentLink.objects.get_or_create(
                parent=request.user,
                student=student,
                defaults={"relationship": relationship[:50]},
            )
            messages.success(request, f"Linked to {student.username}.")
            return redirect("portals:parent")

    return render(request, "portals/link_child.html", {})
