from django import forms
from .models import Country, Language, ProgrammingLanguage, Category


class SignupForm(forms.Form):
    username = forms.CharField(label="", help_text="", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    repeat_password = forms.CharField(label="", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
    email = forms.EmailField(label="", help_text="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), label="", help_text="", empty_label='Country')
    language = forms.ModelChoiceField(queryset=Language.objects.all().order_by('name'), label="", help_text="", empty_label='Language')
    programming_language = forms.ModelChoiceField(queryset=ProgrammingLanguage.objects.all().order_by('name'), label="", help_text="", empty_label='Prefered programming language')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='', help_text='', initial=0)
