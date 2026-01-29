from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Grade, Domain, Standard, Lesson

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},   
    }
    fields = ('title', 'content')

class StandardAdmin(admin.ModelAdmin):
    list_display = ("code", "domain")
    inlines = [LessonInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'standard', 'created_at']
    list_display_links = ['title']  # This makes it clickable
    list_filter = ['standard__domain__grade', 'standard__domain']
    search_fields = ['title', 'content']



admin.site.register(Grade)
admin.site.register(Domain)
admin.site.register(Standard, StandardAdmin)
admin.site.register(Lesson, LessonAdmin)