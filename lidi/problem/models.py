from django.db import models
from datetime import date
import signup

class Problem(models.Model):
	name = models.CharField(max_length=200)
	desc = models.CharField(max_length=6000)
	difficulty = models.IntegerField()
	submitted_by = models.ForeignKey(signup.models.User)

class Submission(models.Model):
	user = models.ForeignKey(signup.models.User)
	problem = models.ForeignKey(Problem)
	date = models.CharField(max_length=10, default='{0}/{1}/{2}'.format(date.today().year, date.today().month, date.today().day))
	tries = models.IntegerField(default=0)
	tries_until_correct = models.IntegerField(default=0)
	grade = models.IntegerField(default=-1)
	sub_file = models.CharField(max_length=100)
