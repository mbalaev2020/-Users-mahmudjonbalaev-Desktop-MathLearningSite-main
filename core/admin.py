from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Classroom, ParentLink

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # grade exists on User per the model above
    list_display = ("username", "email", "role", "grade", "is_active", "last_login")
    list_filter  = ("role", "is_active", "is_staff")
    search_fields = ("username", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Role & Profile", {"fields": ("role", "grade")}),
    )

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "student_count")
    filter_horizontal = ("students",)

    def student_count(self, obj): return obj.students.count()
    student_count.short_description = "Students"

    # Teachers: only their own; admins/staff: all
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or getattr(request.user, "role", "") != "teacher":
            return qs
        return qs.filter(teacher=request.user)

    def has_change_permission(self, request, obj=None):
        if obj and getattr(request.user, "role", "") == "teacher":
            return obj.teacher_id == request.user.id
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and getattr(request.user, "role", "") == "teacher":
            return obj.teacher_id == request.user.id
        return super().has_delete_permission(request, obj)


@admin.register(ParentLink)
class ParentLinkAdmin(admin.ModelAdmin):
    list_display = ("parent", "student", "relationship")
    search_fields = ("parent__username", "student__username", "relationship")
