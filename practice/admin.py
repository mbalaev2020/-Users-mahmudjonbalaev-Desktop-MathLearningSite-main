from django.contrib import admin
from .models import SkillSet, PracticeQuestion, Hint

class HintInline(admin.TabularInline):
    model = Hint
    extra = 0

class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "skill_set", "correct_answer")
    inlines = [HintInline]

admin.site.register(SkillSet)
admin.site.register(PracticeQuestion, PracticeQuestionAdmin)
