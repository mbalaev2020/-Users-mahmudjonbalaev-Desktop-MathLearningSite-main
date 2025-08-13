from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class BaseSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)  # passwords handled by UserCreationForm

    # Never trust role from POST; set in save()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ("username", "email", "password1", "password2"):
            self.fields[f].widget.attrs.update({"class": "form-control"})

class StudentSignUpForm(BaseSignUpForm):
    grade = forms.IntegerField(min_value = 1, max_value = 12, required = False)

    def save(self, commit = True):
        user = super().save(commit = False)
        user.role = "student"
        user.grade = self.cleaned_data.get("grade")
        if commit:
            user.save()
        return user

class TeacherSignUpForm(BaseSignUpForm):
    def save(self, commit = True):
        user = super().save(commit = False)
        user.role = "teacher"
        user.is_staff = True
        user.is_superuser = False
        if commit:
            user.save()
        return user

class ParentSignUpForm(BaseSignUpForm):
    relationship = forms.CharField(max_length = 50, required = False, help_text = "e.g., Mother, Father, Guardian")

    def save(self, commit = True):
        user = super().save(commit = False)
        user.role = "parent"
        if commit:
            user.save()
        #relationship is used later if they link a child
        user._relationship = self.cleaned_data.get("relationship")
        return user