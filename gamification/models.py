from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Plant(models.Model):
    STAGE_CHOICES = [
        ('seedling', 'Seedling'),
        ('budding', 'Budding'),
        ('bloomed', 'Fully Bloomed'),
        ('tree', 'Grade Tree'),
        ('rare', 'Rare/Exotic')
    ]

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.CharField(max_length = 100) # operations...
    growth_stage = models.CharField(max_length = 20, choices = STAGE_CHOICES, default = 'seedling')
    last_update = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.growth_stage})"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.CharField(max_length = 100)
    percent_complete = models.FloatField(default = 0.0)
    skills_mastered = models.PositiveIntegerField(default = 0)
    last_update = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.percent_complete:.1f}%"

class LoginStreak(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    current_streak = models.PositiveIntegerField(default = 0)
    last_login = models.DateField(null = True, blank = True)
    longest_streak = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak}-day streak"

class Badge(models.Model):
    BADGE_CHOICES = [
        ('first_login', 'First Login'),
        ('category_complete', 'Completed a Category'),
        ('grade_complete', 'Completed a Grade'),
        ('streak_5', '5-Day Streak'),
        ('rare_plant', "Rare/Exotic Achievement"),
    ]

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    badge_type = models.CharField(max_length = 100, choices = BADGE_CHOICES)
    unlocked_on = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('user', 'badge_type')

    def __str__(self):
        return f"{self.user.username} - {self.get_badge_type_display()}"

class GardenState(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    health_score = models.PositiveIntegerField(default = 100)
    visual_theme = models.CharField(max_length = 50, default = 'default') #spring, fall

    def __str__(self):
        return f"{self.user.username}  Garden - {self.health_score}% health"
