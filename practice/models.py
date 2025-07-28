from django.db import models
from django.conf import settings
from curriculum.models import Standard

class SkillSet(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    related_standards = models.ManyToManyField(Standard)

    def __str__(self):
        return self.title

class PracticeQuestion(models.Model):
    skill_set = models.ForeignKey(SkillSet, on_delete=models.CASCADE, related_name="practice_questions")
    question_text = models.TextField()
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    ANSWER_CHOICES = [(x, x) for x in "ABCD"]
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation_text = models.TextField(blank=True)

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
    selected = models.CharField(max_length=1, choices=[(x, x) for x in "ABCD"])
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "question")

#track user
class UserSkillProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill_set = models.ForeignKey(SkillSet, on_delete=models.CASCADE)
    is_mastered = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "skill_set")