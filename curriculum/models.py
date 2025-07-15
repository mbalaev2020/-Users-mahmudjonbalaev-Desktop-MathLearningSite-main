from django.db import models
from django.utils.text import slugify

class Grade(models.Model):
    level = models.PositiveSmallIntegerField(unique=True)   # 3-8, 9(SHSAT), 10(SAT)

    class Meta:
        ordering = ["level"]

    def __str__(self):
        return f"Grade {self.level}"


class Domain(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="domains")
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(max_length=120, blank=True)

    class Meta:
        unique_together = ("grade", "name")
        ordering = ["grade", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grade} – {self.name}"


class Standard(models.Model):
    domain      = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="standards")
    code        = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.code


class Lesson(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="lessons")
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    order    = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
