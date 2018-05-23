from django import forms
from signup.models import ProgrammingLanguage


class UploadSolutionForm(forms.Form):
    f = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'upload_file_button'}))
    prog_lang = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all().order_by('name'), label="", \
                                       help_text="", empty_label='Programming language')
