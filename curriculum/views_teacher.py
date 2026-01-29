from django.contrib import messages
from django.shortcuts import redirect, render
from core.decorators import role_required
from .forms import LessonForm

@role_required("teacher")
def teacher_create_lesson(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, f"Lesson '{lesson.title}' created.")
            return redirect("curriculum:teacher_create_lesson")
    else:
        form = LessonForm()
    return render(request, "curriculum/teacher_create_lesson.html", {"form": form})
