from django.shortcuts import render, redirect
from curriculum.models import Grade
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm

def register_view(request):
    """
      /register/ shows a tabbed chooser with all three forms.
      Still supports ?role=teacher|parent|student deep links.
      """
    role = (request.GET.get("role") or "").lower()
    if role == "teacher":
        return redirect("register_teacher")
    if role == "parent":
        return redirect("register_parent")
    if role == "student":
        return redirect("register_student")

    # Render the 3 forms on one page; each posts to its own endpoint.
    ctx = {
        "student_form": StudentSignUpForm(),
        "teacher_form": TeacherSignUpForm(),
        "parent_form": ParentSignUpForm(),
    }
    return render(request, "core/register_tabs.html", ctx)

def home_view(request):
    grades = Grade.objects.all()

    user = request.user
    show_teacher_card = False
    if user.is_authenticated:
        # 1) If you use Groups
        in_teacher_group = user.groups.filter(name="teacher").exists()

        # 2) Also support a role field if your custom user has one
        has_teacher_role = getattr(user, "role", None) == "teacher"

        show_teacher_card = in_teacher_group or has_teacher_role

    return render(request, "core/home.html", {
        "grades": grades,
        "show_teacher_card": show_teacher_card,
    })
def grades_view(request, grade_id):
    """Accepts '3'..'8', 'SHSAT'->9, 'SAT'->10; loads Grade and related content."""
    s = str(grade_id).strip().upper()
    if s == "SHSAT":
        level = 9
    elif s == "SAT":
        level = 10
    else:
        try:
            level = int(s)
        except ValueError:
            return render(request, "core/grade_detail.html", {
                "page_title": "Not Found",
                "description": "Invalid grade.",
                "grade": None,
            })

    grade = (
        Grade.objects
        .prefetch_related("domains__standards")
        .filter(level=level)
        .first()
    )

    if not grade:
        return render(request, "core/grade_detail.html", {
            "page_title": "Not Found",
            "description": "No data available for this grade.",
            "grade": None,
        })

    return render(request, "core/grade_detail.html", {
        "grade": grade,
        "page_title": str(grade),
        "description": f"Explore domains and standards for {grade}.",
    })
