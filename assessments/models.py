from django.db import models
from django.conf import settings
from curriculum.models import Grade, Standard

class Test(models.Model):
    TYPE = [
        ("diagnostic", "Diagnostic"),
        ("sectional",  "Sectional"),
        ("review",     "Monthly Review"),
        ("shsat",      "SHSAT Prep"),
        ("sat",        "SAT Prep"),
    ]
    title = models.CharField(max_length=200)
    test_type = models.CharField(max_length=12, choices=TYPE)
    grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL)
    standards = models.ManyToManyField(Standard, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[(x, x) for x in "ABCD"])
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.test} – Q{self.pk}"

class UserTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "test")

class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1, choices=[(x, x) for x in "ABCD"])
    is_correct = models.BooleanField()