from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Plant(models.Model):
    STAGE_CHOICES = [
        ("seedling", "Seedling"),
        ("budding", "Budding"),
        ("bloomed", "Fully Bloomed"),
        ("tree", "Grade Tree"),
        ("rare", "Rare/Exotic"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)  # e.g., "Grade 3 – Fractions"
    growth_stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="seedling")

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.growth_stage})"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    percent_complete = models.FloatField(default=0.0)
    skills_mastered = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "category")

class LoginStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    last_login_day = models.DateField(null=True, blank=True)

class Badge(models.Model):
    BADGE_TYPES = [
        ("streak_7", "7-Day Streak"),
        ("streak_30", "30-Day Streak"),
        ("all_skills_grade", "All Skills (Grade)"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50, choices=BADGE_TYPES)
    unlocked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge_type")

class GardenState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    health_score = models.PositiveIntegerField(default=0)  # 0–100
    visual_theme = models.CharField(max_length=50, default="spring")
