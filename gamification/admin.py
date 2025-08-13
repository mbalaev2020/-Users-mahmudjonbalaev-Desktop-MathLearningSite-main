from django.contrib import admin
from .models import Plant, LoginStreak, Badge, GardenState

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    # use callables so admin doesn’t crash if fields don’t exist
    list_display = ("user_safe", "category_safe", "percent_complete_safe", "stage_safe", "updated_at_safe")
    search_fields = ("user__username",)

    def user_safe(self, obj):
        return getattr(obj, "user", None)
    user_safe.short_description = "User"

    def category_safe(self, obj):
        return getattr(obj, "category", None)
    category_safe.short_description = "Category"

    def percent_complete_safe(self, obj):
        return getattr(obj, "percent_complete", None)
    percent_complete_safe.short_description = "Percent Complete"

    def stage_safe(self, obj):
        return getattr(obj, "stage", None)
    stage_safe.short_description = "Stage"

    def updated_at_safe(self, obj):
        return getattr(obj, "updated_at", None)
    updated_at_safe.short_description = "Updated"

@admin.register(LoginStreak)
class LoginStreakAdmin(admin.ModelAdmin):
    list_display = ("user_safe", "current_streak_safe", "longest_streak_safe", "last_login_safe")
    search_fields = ("user__username",)

    def user_safe(self, obj): return getattr(obj, "user", None)
    user_safe.short_description = "User"
    def current_streak_safe(self, obj): return getattr(obj, "current_streak", None)
    current_streak_safe.short_description = "Current Streak"
    def longest_streak_safe(self, obj): return getattr(obj, "longest_streak", None)
    longest_streak_safe.short_description = "Longest Streak"
    def last_login_safe(self, obj): return getattr(obj, "last_login", None)
    last_login_safe.short_description = "Last Login"

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("user_safe", "badge_type_safe", "unlocked_on_safe")
    search_fields = ("user__username",)

    def user_safe(self, obj): return getattr(obj, "user", None)
    user_safe.short_description = "User"
    def badge_type_safe(self, obj): return getattr(obj, "badge_type", None)
    badge_type_safe.short_description = "Badge"
    def unlocked_on_safe(self, obj): return getattr(obj, "unlocked_on", None)
    unlocked_on_safe.short_description = "Unlocked On"

@admin.register(GardenState)
class GardenStateAdmin(admin.ModelAdmin):
    list_display = ("user_safe", "health_score_safe", "visual_theme_safe")
    search_fields = ("user__username",)

    def user_safe(self, obj): return getattr(obj, "user", None)
    user_safe.short_description = "User"
    def health_score_safe(self, obj): return getattr(obj, "health_score", None)
    health_score_safe.short_description = "Health Score"
    def visual_theme_safe(self, obj): return getattr(obj, "visual_theme", None)
    visual_theme_safe.short_description = "Theme"
