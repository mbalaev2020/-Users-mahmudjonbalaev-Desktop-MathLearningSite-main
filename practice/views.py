from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils import evaluate_skillset_readiness
from .models import SkillSet, PracticeQuestion, Attempt


def skillset_list(request):
    return render(request, "practice/skillset_list.html", {"skillsets": SkillSet.objects.all()})

@login_required
def practice_start(request, skillset_id):
    skillset = get_object_or_404(SkillSet, pk=skillset_id)

    # Only count questions the user got right
    correct = Attempt.objects.filter(
        user=request.user,
        question__skill_set=skillset,
        is_correct=True
    ).values_list("question_id", flat=True)

    q = PracticeQuestion.objects.filter(skill_set=skillset).exclude(id__in=correct).first()

    if q:
        return redirect("practice:question", skillset_id=skillset.id, q_id=q.id)

    return render(request, "practice/completed.html", {"skillset": skillset})


@login_required
def question_view(request, skillset_id, q_id):
    skillset = get_object_or_404(SkillSet, pk=skillset_id)
    question = get_object_or_404(PracticeQuestion, pk=q_id, skill_set=skillset)

    # Count total and correct questions for progress bar
    total = PracticeQuestion.objects.filter(skill_set=skillset).count()
    correct = Attempt.objects.filter(user=request.user, question__skill_set=skillset, is_correct=True).count()
    remaining = total - correct

    if request.method == "POST":
        sel = request.POST.get("choice")
        is_ok = sel == question.correct_answer

        Attempt.objects.update_or_create(
            user=request.user, question=question,
            defaults={"selected": sel, "is_correct": is_ok},
        )

        if not is_ok:
            return render(request, "practice/question.html", {
                "skillset": skillset, "question": question,
                "selected": sel, "is_correct": False,
                "show_result": True,
                "message": "Try again until you get it right!",
                "progress": {"total": total, "correct": correct, "remaining": remaining}
            })

        next_q = PracticeQuestion.objects.filter(
            skill_set=skillset
        ).exclude(
            id__in=Attempt.objects.filter(user=request.user, is_correct=True).values_list("question_id", flat=True)
        ).first()

        if not next_q:
            from .models import UserSkillProgress
            UserSkillProgress.objects.update_or_create(
                user=request.user, skill_set=skillset,
                defaults={"is_mastered": True}
            )
            return render(request, "practice/completed.html", {"skillset": skillset})

        return redirect("practice:question", skillset_id=skillset.id, q_id=next_q.id)

    return render(request, "practice/question.html", {
        "skillset": skillset,
        "question": question,
        "progress": {"total": total, "correct": correct, "remaining": remaining}
    })

class SkillSetReadinessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, skillset_id):
        skillset = SkillSet.objects.get(pk=skillset_id)
        status = evaluate_skillset_readiness(request.user, skillset)

        # Return HTML for HTMX
        html = render_to_string("practice/partials/readiness_result.html", {
            "status": status
        })
        return HttpResponse(html)