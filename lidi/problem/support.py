import os
from django.core.exceptions import ObjectDoesNotExist
from signup.models import User
from .models import Submission
from datetime import date

def handle_solution(f, problem_id, user, lang):
	directory = os.popen('echo $CG_FILES_UPLOADED').read().strip()
	problem_dir = "{0}/{1}/{2}".format(directory, user, problem_id)

	try:
		os.mkdir(problem_dir)
	except OSError:
		pass # directory already exists

	_, end = f.name.split('.')
	f_local = '{2}_{0}.{1}'.format(user, end, problem_id)
	with open('{0}/{1}'.format(problem_dir, f_local), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	# Grade the task using grade.sh
	grade = os.popen('bash problem/grade.sh {0} {1}'.format(f_local, lang)).read().strip()

	# Add submission
	user_id = User.objects.get(username=user).id
	today = date.today()
	today_str = '{0}/{1}/{2}'.format(today.year, today.month, today.day)
	try:
		submission = Submission.objects.get(user=user_id, problem=problem_id)
		submission.tries += 1
		if grade >= submission.grade:
			submission.grade = grade
			submission.date = today_str
	except ObjectDoesNotExist:
		submission = Submission()
		submission.user_id = user_id
		submission.problem_id = problem_id
		submission.grade = grade
		submission.date = today_str
		submission.tries = 1
	finally:
		submission.save()
	return grade
