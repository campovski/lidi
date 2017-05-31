from django import forms
from .models import Country, Language, ProgrammingLanguage

class SignupForm(forms.Form):
	username = forms.CharField(label="Username", help_text="", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(label="Password", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	repeat_password = forms.CharField(label="Repeat password", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	email = forms.EmailField(label="Email", help_text="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
	country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'))
	language = forms.ModelChoiceField(queryset=Language.objects.all().order_by('name'))
	programming_language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all().order_by('name'))
