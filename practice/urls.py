from django.urls import path
from . import views

app_name = "practice"

urlpatterns = [
    path("skills/", views.skillset_list, name="skillset_list"),
    path("skill/<int:skillset_id>/start/", views.practice_start, name="start"),
    path("skill/<int:skillset_id>/q/<int:q_id>/", views.question_view, name="question"),
]