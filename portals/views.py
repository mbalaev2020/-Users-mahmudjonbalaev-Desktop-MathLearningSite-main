from django.shortcuts import render
from core.decorators import role_required
from practice.models import UserSkillProgress
from assessments.models import Test, UserTest
from core.models import Classroom, ParentLink

@role_required('student')
def student_dashboard(request):
    progress = UserSkillProgress.objects.filter(user=request.user).select_related("skill_set")
    tests = UserTest.objects.filter(user=request.user).select_related("test")
    return render(request, "portals/student_dashboard.html", {"progress": progress, "tests": tests})

@role_required('teacher')
def teacher_dashboard(request):
    classes = Classroom.objects.filter(teacher=request.user).prefetch_related("students")
    return render(request, "portals/teacher_dashboard.html", {"classes": classes})


@role_required("parent")
def parent_dashboard(request):
    links = ParentLink.objects.select_related("student").filter(parent=request.user)

    # Prefetch each child's progress & recent tests
    student_ids = [l.student_id for l in links]
    progress = UserSkillProgress.objects.filter(user_id__in=student_ids).select_related("skill_set")
    tests = UserTest.objects.filter(user_id__in=student_ids).select_related("test")

    # Map by student id for easy lookup in template
    prog_by_student = {}
    for p in progress:
        prog_by_student.setdefault(p.user_id, []).append(p)
    tests_by_student = {}
    for t in tests:
        tests_by_student.setdefault(t.user_id, []).append(t)

    # Attach summaries onto links (so template stays simple)
    for l in links:
        l._progress = prog_by_student.get(l.student_id, [])
        l._tests = tests_by_student.get(l.student_id, [])

    return render(request, "portals/parent_dashboard.html", {"links": links})

