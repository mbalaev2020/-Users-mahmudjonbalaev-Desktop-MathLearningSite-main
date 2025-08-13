from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("parent",  "Parent"),
        ("admin",   "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    # Optional but used by admin/templates; safe to add
    grade = models.PositiveSmallIntegerField(null=True, blank=True)

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    # give teacher a unique reverse accessor
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='classes_taught',
    )
    # students should be ManyToMany and have a distinct reverse accessor
    students = models.ManyToManyField(
        User,
        related_name='classes',
        limit_choices_to={'role': 'student'},
        blank=True,
    )

    def __str__(self):
        return self.name

class ParentLink(models.Model):
    parent = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='children_links',
        limit_choices_to={'role': 'parent'}
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='parent_links',
        limit_choices_to={'role': 'student'}
    )
    relationship = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ("parent", "student")
