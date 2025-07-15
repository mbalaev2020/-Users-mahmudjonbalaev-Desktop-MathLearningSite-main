from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Grade, Domain, Standard, Lesson

class GradeListView(ListView):
    model = Grade
    template_name = "curriculum/grade_list.html"
    context_object_name = "grades"

class DomainListView(ListView):
    template_name = "curriculum/domain_list.html"
    context_object_name = "domains"

    def get_queryset(self):
        self.grade = get_object_or_404(Grade, level=self.kwargs["grade_level"])
        return self.grade.domains.all()

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