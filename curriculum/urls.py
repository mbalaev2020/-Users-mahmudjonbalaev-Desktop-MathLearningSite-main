from django.urls import path
from .views import GradeListView, DomainListView, StandardListView, LessonDetailView, StandardDetailView

app_name = "curriculum"

urlpatterns = [
    path("", GradeListView.as_view(), name="grade_list"),
    path("<int:grade_level>/", DomainListView.as_view(), name="domain_list"),
    path("<int:grade_level>/<slug:domain_slug>/", StandardListView.as_view(), name="standard_list"),
    path("<int:grade_level>/<slug:domain_slug>/lesson/<int:pk>/", LessonDetailView.as_view(), name="lesson_detail"),
    path("<int:grade_level>/<slug:domain_slug>/standard/<int:pk>/", StandardDetailView.as_view(), name="standard_detail"),
]