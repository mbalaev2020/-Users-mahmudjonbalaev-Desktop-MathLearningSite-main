from django import forms
from .models import SkillSet

class CSVPracticeUploadForm(forms.Form):
    csv_file = forms.FileField(required=True)
    default_skill_set = forms.ModelChoiceField(queryset=SkillSet.objects.none(), required=False)
    replace_existing = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["default_skill_set"].queryset = SkillSet.objects.all()

class PDFPracticeUploadForm(forms.Form):
    pdf_file = forms.FileField(required=True)
    skillset_title = forms.CharField(required=True)
    standard_code = forms.CharField(required=True)
    reset = forms.BooleanField(required=False)
