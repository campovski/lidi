from django import forms

class UploadSolutionForm(forms.Form):
	f = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'upload_file_button'}))
