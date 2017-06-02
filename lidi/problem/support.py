import os

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
	return grade
