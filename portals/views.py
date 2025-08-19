from django.shortcuts import render
from core.decorators import role_required
from practice.models import UserSkillProgress, SkillSet
from assessments.models import Test, UserTest
from core.models import Classroom, ParentLink
from django.utils import timezone

@role_required('student')
def student_dashboard(request):
    progress = UserSkillProgress.objects.filter(user=request.user).select_related("skill_set")
    tests = UserTest.objects.filter(user=request.user).select_related("test")
    return render(request, "portals/student_dashboard.html", {"progress": progress, "tests": tests})

def teacher_dashboard(request):
    """
    Context provided:
      classes: [
        {"id": ..., "name": "...", "students": [
            {"id": ..., "username": "...", "grade": ..., "last_login": ..., "mastery_percent": int}
        ]}
      ]
      avg_mastery: average mastery % across all listed students (or None)
      active_today: number of students with last_login == today
      tests_unlocked: total count of unlocked tests across all listed students
    """
    # Teacher's classes + students
    class_qs = Classroom.objects.filter(teacher=request.user).prefetch_related("students")

    # Denominator for mastery percent (avoid divide-by-zero)
    total_skillsets = SkillSet.objects.count() or 1

    today = timezone.localdate()
    classes = []

    sum_mastery = 0
    student_count = 0
    active_today = 0
    tests_unlocked = 0

    # Cache tests (avoid repeated queries in the loop)
    all_tests = list(Test.objects.all())

    for c in class_qs:
        students_list = []
        for u in c.students.all():
            # mastery % = (# mastered skillsets) / (total skillsets) * 100
            mastered = UserSkillProgress.objects.filter(user=u, is_mastered=True).count()
            mastery_percent = round((mastered / total_skillsets) * 100)

            # aggregate metrics
            sum_mastery += mastery_percent
            student_count += 1
            if getattr(u, "last_login", None) and u.last_login.date() == today:
                active_today += 1

            # unlocked tests for this student
            for t in all_tests:
                if t.is_unlocked_for(u):
                    tests_unlocked += 1

            students_list.append({
                "id": u.id,
                "username": u.username,
                "grade": getattr(u, "grade", None),
                "last_login": u.last_login,
                "mastery_percent": mastery_percent,
            })

        classes.append({
            "id": c.id,
            "name": c.name,
            "students": students_list,  # plain list for simple templating
        })

    avg_mastery = round(sum_mastery / student_count, 1) if student_count else None

    return render(request, "portals/teacher_dashboard.html", {
        "classes": classes,
        "avg_mastery": avg_mastery,
        "active_today": active_today,
        "tests_unlocked": tests_unlocked,
    })

@role_required("parent")
def parent_dashboard(request):
    links = ParentLink.objects.select_related("student").filter(parent=request.user)
    student_ids = [l.student_id for l in links]
    progress = UserSkillProgress.objects.filter(user_id__in=student_ids).select_related("skill_set")
    tests = UserTest.objects.filter(user_id__in=student_ids).select_related("test")
    return render(
        request,
        "portals/parent_dashboard.html",
        {"links": links, "progress": progress, "tests": tests},
    )
