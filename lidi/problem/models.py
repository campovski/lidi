from datetime import date

from django.db import models

import signup


class Problem(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=6000)
    difficulty = models.IntegerField()
    submitted_by = models.ForeignKey(signup.models.User, related_name='submitted_by')
    submitted_on = models.DateField()
    solved_by_how_many = models.IntegerField(default=0)
    first_solved_by = models.ForeignKey(signup.models.User, related_name='first_solved_by', null=True)
    first_solved_on = models.DateField(null=True)
    last_successful_try = models.DateField(null=True)

    def __str__(self):
        return self.name


class Submission(models.Model):
    user = models.ForeignKey(signup.models.User)
    problem = models.ForeignKey(Problem)
    date = models.CharField(max_length=10, default='{0}/{1}/{2}'.format(date.today().year, date.today().month, date.today().day))
    tries = models.IntegerField(default=0)
    tries_until_correct = models.IntegerField(default=0)
    grade = models.IntegerField(default=-1)
    sub_file = models.CharField(max_length=100)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.problem)
