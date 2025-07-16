# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, dashboard_view, home_view, grades_view

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("grade/<int:grade_number>/", grades_view, name="grade_detail"),
]