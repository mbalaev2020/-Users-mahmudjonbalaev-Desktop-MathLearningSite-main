from django.urls import path
from . import views

app_name = "portals"
urlpatterns = [
    path("student/", views.student_dashboard, name="student"),
    path("teacher/", views.teacher_dashboard, name="teacher"),
    path("parent/",  views.parent_dashboard,  name="parent"),
]
