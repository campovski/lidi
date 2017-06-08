import os
import re

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
	rewrite_times('{0}/time'.format(problem_dir))

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


def get_solutions_and_times(username, problem_id):
	outputs_l = []
	outputs_h = []

	user_id = User.objects.get(username=username).id
	up_dir = '{0}/{1}/{2}'.format(os.popen('echo $CG_FILES_UPLOADED').read().strip(), username, problem_id)

	for i in range(10):
		f = open('{0}/best_out/out_{1}_{2}_{3}'.format(up_dir, problem_id, username, i))
		outputs_h.append(f.read().replace('\n', '<br>'))
		f.close()

		f = open('{0}/last_out/out_{1}_{2}_{3}'.format(up_dir, problem_id, username, i))
		outputs_l.append(f.read().replace('\n', '<br>'))
		f.close()

	# Read solutions to problems.
	prog_name = os.popen('ls {0}/prog'.format(up_dir)).read().strip()
	f = open('{0}/prog/{1}'.format(up_dir, prog_name))
	program = f.read().replace('\n', '<br>')
	f.close()

	# Read times.
	f = open('{0}/prog/times'.format(up_dir))
	times = f.readlines()
	f.close()

	return outputs_l, outputs_h, program, times


def rewrite_times(f_times):
	f = open(f_times)
	pattern = re.compile(r'(?<=real\t)\d+m\d+.\d\d\ds')
	times = ''
	for line in f:
		tmp = pattern.search(line)
		if tmp != None:
			times += '{0}\n'.format(tmp.group())
	f.close()
	
	f = open(f_times, 'w')
	f.write(times)
	f.close()
