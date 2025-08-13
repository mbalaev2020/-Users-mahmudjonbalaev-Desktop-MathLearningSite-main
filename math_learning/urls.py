from django.contrib import admin
from django.urls import include, path
from gamification.views import dashboard_page
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Core site (home, grades, register shim, per-role register, link-child)
    path("", include("core.urls")),
    # Portals (student/teacher/parent dashboards)
    path("portal/", include(("portals.urls", "portals"), namespace="portals")),
    # Built-in auth (so /accounts/login and /accounts/logout also work)
    path("accounts/login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    # Apps used by header links
    path("practice/", include(("practice.urls", "practice"), namespace="practice")),
    path("assessments/", include(("assessments.urls", "assessments"), namespace="assessments")),
    path("gamification/", include(("gamification.urls", "gamification"), namespace="gamification")),
    # Alias so {% url 'gamification-page' %} resolves
    path("gamification/page/", dashboard_page, name="gamification-page"),
    # Curriculum (namespaced so grade_detail template can link standards)
    path("curriculum/", include(("curriculum.urls", "curriculum"), namespace="curriculum")),
    # Admin
    path("admin/", admin.site.urls),
]
