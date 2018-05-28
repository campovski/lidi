from django import forms


class LoginForm(forms.Form):
    user = forms.CharField(label="", help_text="", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username or email'}))
    password = forms.CharField(label="", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class PasswordResetEmailForm(forms.Form):
    user = forms.CharField(label="", help_text="", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username or email'}))


class PasswordResetChangePasswordForm(forms.Form):
    username = forms.CharField(label="", help_text="", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label="", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="", help_text="", max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
