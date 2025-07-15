from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Test, Question, UserTest, UserAnswer

@login_required
def test_list(request):
    return render(request, "assessments/test_list.html", {"tests": Test.objects.all()})

@login_required
def test_start(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    ut, _ = UserTest.objects.get_or_create(user=request.user, test=test)

    if ut.completed:
        return redirect("assessments:summary", ut.id)

    answered = ut.answers.values_list("question_id", flat=True)
    q = test.questions.exclude(id__in=answered).first()
    if q:
        return redirect("assessments:question", ut.id, q.id)

    correct = ut.answers.filter(is_correct=True).count()
    ut.score = int(correct / test.questions.count() * 100)
    ut.completed = True
    ut.finished_at = timezone.now()
    ut.save()
    return redirect("assessments:summary", ut.id)

@login_required
def question_view(request, ut_id, q_id):
    ut = get_object_or_404(UserTest, pk=ut_id, user=request.user)
    q = get_object_or_404(Question, pk=q_id, test=ut.test)

    if request.method == "POST":
        sel = request.POST.get("choice")
        UserAnswer.objects.update_or_create(
            user_test=ut, question=q,
            defaults={"selected": sel, "is_correct": sel == q.correct_answer},
        )
        return redirect("assessments:start", ut.test.id)

    return render(request, "assessments/question.html", {"question": q, "ut": ut})

@login_required
def summary_view(request, ut_id):
    ut = get_object_or_404(UserTest, pk=ut_id, user=request.user)
    return render(request, "assessments/summary.html", {"ut": ut, "answers": ut.answers.select_related("question")})