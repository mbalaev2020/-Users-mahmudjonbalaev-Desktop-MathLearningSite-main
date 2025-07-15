from django.db import models
from django.contrib.auth.models import AbstractUser
from curriculum.models import Grade

class User(AbstractUser):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    is_student = models.BooleanField(default=True) # use to seprate roles later

    def __str__(self):
        return self.username
