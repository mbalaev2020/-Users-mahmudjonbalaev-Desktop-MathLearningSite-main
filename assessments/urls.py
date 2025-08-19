from django.urls import path
from . import views, views_teacher


app_name = "assessments"
urlpatterns = [
    path("", views.test_list, name="list"),
    path("<int:test_id>/start/", views.test_start, name="start"),
    path("ut/<int:ut_id>/q/<int:q_id>/", views.question_view, name="question"),
    path("ut/<int:ut_id>/summary/", views.summary_view, name="summary"),
    path("teacher/create-test/", views_teacher.teacher_create_test, name="teacher_create_test"),
    path("teacher/bulk-test-upload/", views_teacher.teacher_bulk_test_upload, name="teacher_bulk_test_upload"),
]
