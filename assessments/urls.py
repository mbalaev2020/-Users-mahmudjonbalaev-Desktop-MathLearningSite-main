from django.urls import path
from . import views

app_name = "assessments"
urlpatterns = [
    path("", views.test_list, name="list"),
    path("<int:test_id>/start/", views.test_start, name="start"),
    path("ut/<int:ut_id>/q/<int:q_id>/", views.question_view, name="question"),
    path("ut/<int:ut_id>/summary/", views.summary_view, name="summary"),
]
