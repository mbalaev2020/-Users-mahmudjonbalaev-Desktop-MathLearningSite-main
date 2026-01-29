from django.db import models
from django.conf import settings
from curriculum.models import Standard

class SkillSet(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    related_standards = models.ManyToManyField(Standard, blank=True)

    def __str__(self):
        return self.title

class PracticeQuestion(models.Model):
    skill_set = models.ForeignKey(SkillSet, on_delete=models.CASCADE, related_name="practice_questions")
    question_text = models.TextField()
    choice_a = models.CharField(max_length=255, blank=True)
    choice_b = models.CharField(max_length=255, blank=True)
    choice_c = models.CharField(max_length=255, blank=True)
    choice_d = models.CharField(max_length=255, blank=True)
    correct_answer = models.CharField(max_length=255)  # store the text or "A/B/C/D"
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.question_text[:50]

class Hint(models.Model):
    question = models.ForeignKey(PracticeQuestion, on_delete=models.CASCADE, related_name="hints")
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(PracticeQuestion, on_delete=models.CASCADE)
    selected = models.CharField(max_length=255)  # store "A/B/C/D" or text
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
#track user
class UserSkillProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill_set = models.ForeignKey(SkillSet, on_delete=models.CASCADE)
    is_mastered = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "skill_set")