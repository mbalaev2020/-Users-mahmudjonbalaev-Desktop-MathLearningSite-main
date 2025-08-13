# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, home_view, grades_view
from . import views_auth

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    # Provide root-level login/logout that base.html expects
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    # Grades
    path("grade/<slug:grade_id>/", grades_view, name="grade_detail"),
    # Per-role registration
    path("register/student/", views_auth.register_student, name="register_student"),
    path("register/teacher/", views_auth.register_teacher, name="register_teacher"),
    path("register/parent/",  views_auth.register_parent,  name="register_parent"),
    path("link-child/",       views_auth.link_child,       name="link_child"),


]
