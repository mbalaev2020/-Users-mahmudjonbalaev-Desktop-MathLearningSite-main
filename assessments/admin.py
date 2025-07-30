from django.contrib import admin
from .models import Test, Question, UserTest, UserAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "test_type", "grade")
    inlines = [QuestionInline]
    filter_horizontal = ("standards",)