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

	# Grade the task using agrader.sh
	grader_out = os.popen('bash problem/bash/agrader.sh {0} {1}'.format(f_local, lang)).read()
	grade = int(grader_out.strip().split('\n')[-1])
#	errors = grader_out.strip().split('\n')[-2].split()

	# Add submission
	user = User.objects.get(username=user)
	today = date.today()
	today_str = '{0}/{1}/{2}'.format(today.year, today.month, today.day)
	try:
		submission = Submission.objects.get(user=user.id, problem=problem_id)
		submission.tries += 1
		if grade > submission.grade:
			submission.grade = grade
			submission.date = today_str

		# Save newer solution with same points.
		if grade >= submission.grade:
			os.system('bash problem/bash/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 1))
		else:
			os.system('bash problem/bash/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 0))

	except ObjectDoesNotExist:
		submission = Submission()
		submission.user_id = user.id
		submission.problem_id = problem_id
		submission.grade = grade
		submission.date = today_str
		submission.tries = 1
		os.system('bash problem/bash/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 1))

	finally:
		if grade == 10 and submission.tries_until_correct == 0:
			submission.tries_until_correct = submission.tries
		submission.save()

	return grade, submission.grade
