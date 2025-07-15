from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import SkillSet, PracticeQuestion, Attempt

def skillset_list(request):
    return render(request, "practice/skillset_list.html", {"skillsets": SkillSet.objects.all()})

@login_required
def practice_start(request, skillset_id):
    skillset = get_object_or_404(SkillSet, pk=skillset_id)
    answered = Attempt.objects.filter(user=request.user, question__skill_set=skillset).values_list("question_id", flat=True)
    q = PracticeQuestion.objects.filter(skill_set=skillset).exclude(id__in=answered).first()
    if q:
        return redirect("practice:question", skillset_id=skillset.id, q_id=q.id)
    return render(request, "practice/completed.html", {"skillset": skillset})

@login_required
def question_view(request, skillset_id, q_id):
    skillset = get_object_or_404(SkillSet, pk=skillset_id)
    question = get_object_or_404(PracticeQuestion, pk=q_id, skill_set=skillset)

    if request.method == "POST":
        sel = request.POST.get("choice")
        is_ok = sel == question.correct_answer
        Attempt.objects.update_or_create(
            user=request.user, question=question,
            defaults={"selected": sel, "is_correct": is_ok},
        )
        context = {"skillset": skillset, "question": question, "selected": sel, "is_correct": is_ok, "show_result": True}
        return render(request, "practice/question.html", context)

    return render(request, "practice/question.html", {"skillset": skillset, "question": question})