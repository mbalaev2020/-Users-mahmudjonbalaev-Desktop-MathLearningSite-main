from django.urls import path
from . import views

app_name = "gamification"

urlpatterns = [
    # Page view (renders the dashboard.html template)
    path("page/", views.dashboard_page, name="gamification-page"),
    # Example API endpoints (keep if you implement them)
    path("dashboard/", views.DashboardAPIView.as_view(), name="dashboard-data"),
    path("streak/", views.StreakUpdateView.as_view(), name="update-streak"),
    path("progress/", views.ProgressUpdateView.as_view(), name="update-progress"),
    path("badges/", views.BadgeListView.as_view(), name="list-badges"),
    path("garden/", views.GardenView.as_view(), name="garden-data"),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("progress/test/<int:test_id>/", views.TestProgressView.as_view(), name="test-progress"),
    path("progress/all/", views.AllTestProgressAPIView.as_view(), name="all-test-progress"),
]
