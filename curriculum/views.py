from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from .models import Grade, Domain, Standard, Lesson
from practice.models import SkillSet
from assessments.models import Test
from practice.utils import has_mastered_standard


class GradeListView(ListView):
    model = Grade
    template_name = "curriculum/grade_list.html"
    context_object_name = "grades"


class DomainListView(ListView):
    template_name = "curriculum/domain_list.html"
    context_object_name = "domains"

    def get_queryset(self):
        self.grade = get_object_or_404(Grade, level=self.kwargs["grade_level"])
        return self.grade.domains.order_by("sort_order")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["grade"] = self.grade
        return ctx


class StandardListView(ListView):
    template_name = "curriculum/standard_list.html"
    context_object_name = "standards"

    def get_queryset(self):
        self.domain = get_object_or_404(
            Domain,
            grade__level=self.kwargs["grade_level"],
            slug=self.kwargs["domain_slug"],
        )
        return self.domain.standards.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["domain"] = self.domain
        ctx["grade"] = self.domain.grade
        return ctx


class StandardDetailView(DetailView):
    model = Standard
    template_name = "curriculum/standard_detail.html"
    context_object_name = "standard"

    def get_object(self):
        return get_object_or_404(
            Standard,
            pk=self.kwargs["pk"],
            domain__grade__level=self.kwargs["grade_level"],
            domain__slug=self.kwargs["domain_slug"],
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # get all SkillSets for this standard
        ctx["skillsets"] = SkillSet.objects.filter(related_standards=self.object)

        # get all Lessons for this standard
        ctx["lessons"] = self.object.lessons.all()

        # check if test should be unlocked
        user = self.request.user
        test = Test.objects.filter(standards=self.object).first()
        ctx["test"] = test
        ctx["test_unlocked"] = False

        if user.is_authenticated and test:
            ctx["test_unlocked"] = has_mastered_standard(user, self.object)

        return ctx


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "curriculum/lesson_detail.html"
    context_object_name = "lesson"

    def get_object(self):
        return get_object_or_404(
            Lesson,
            pk=self.kwargs["pk"],
            standard__domain__grade__level=self.kwargs["grade_level"],
            standard__domain__slug=self.kwargs["domain_slug"],
        )
