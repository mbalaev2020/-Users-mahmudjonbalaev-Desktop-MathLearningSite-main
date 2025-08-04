from django.urls import path
from .views import (
    dashboard_page,           # renders the HTML template
    DashboardAPIView,            # returns JSON dashboard data
    StreakUpdateView,
    ProgressUpdateView,
    BadgeListView,
    GardenView,
    CategoryListView
)




urlpatterns = [
    # Page view (renders the dashboard.html template)
    path("page/", dashboard_page, name="gamification-page"),

    # API endpoints (return JSON)
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard-data"),
    path("streak/", StreakUpdateView.as_view(), name="update-streak"),
    path("progress/", ProgressUpdateView.as_view(), name="update-progress"),
    path("badges/", BadgeListView.as_view(), name="list-badges"),
    path("garden/", GardenView.as_view(), name="garden-data"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
]
