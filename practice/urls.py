from django.urls import path
from . import views
from .views import SkillSetReadinessView

app_name = "practice"

urlpatterns = [
    path("skills/", views.skillset_list, name="skillset_list"),
    path("skill/<int:skillset_id>/start/", views.practice_start, name="start"),
    path("skill/<int:skillset_id>/q/<int:q_id>/", views.question_view, name="question"),
    path("readiness/<int:skillset_id>/", SkillSetReadinessView.as_view(), name="skillset_readiness"),

]