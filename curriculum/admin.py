from django.contrib import admin
from .models import Grade, Domain, Standard, Lesson

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class StandardAdmin(admin.ModelAdmin):
    list_display = ("code", "domain")
    inlines = [LessonInline]

admin.site.register(Grade)
admin.site.register(Domain)
admin.site.register(Standard, StandardAdmin)
admin.site.register(Lesson)