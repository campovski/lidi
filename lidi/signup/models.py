from django.db import models
from django.forms import ModelForm


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.EmailField(unique=True, null=False)
    country = models.ForeignKey(Country, null=False)
    language = models.ForeignKey(Language, null=False)
    programming_language = models.ForeignKey(ProgrammingLanguage, null=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    conf_link = models.CharField(max_length=200, default="")
    container_id = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.username


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'country', 'language', 'programming_language']
