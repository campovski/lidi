from django import forms

class UploadSolutionForm(forms.Form):
	f = forms.FileField(label='')
