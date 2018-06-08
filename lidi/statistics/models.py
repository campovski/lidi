from django.db import models

from datetime import date

from signup.models import User


class Achievement(models.Model):
    name = models.TextField(unique=True)
    first_acquired = models.ForeignKey(User, null=True, blank=True)
    date_first_acquired = models.CharField(max_length=10, default='{0}-{1}-{2}'.format(date.today().year, date.today().month, date.today().day), null=True, blank=True)
    number_of_people = models.PositiveIntegerField(default=0)


class UserAchievement(models.Model):
    user = models.ForeignKey(User)
    achievement = models.ForeignKey(Achievement)
    date_acquired = models.CharField(max_length=10, default='{0}-{1}-{2}'.format(date.today().year, date.today().month, date.today().day))


class Rating(models.Model):
    user = models.ForeignKey(User, null=False, unique=True)
    rating = models.PositiveIntegerField(default=0)
