from django import forms
from .models import Test, Question

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "grade", "standards"]

class CSVTestQuestionUploadForm(forms.Form):
    csv_file = forms.FileField(required=True)
    default_test = forms.ModelChoiceField(queryset=Test.objects.none(), required=False)
    replace_existing = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["default_test"].queryset = Test.objects.all()
