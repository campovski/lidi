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
	date = models.DateField(default=date.today)
	tries = models.IntegerField()
	is_solved = models.BooleanField(default=False)
	sub_file = models.CharField(max_length=100)
