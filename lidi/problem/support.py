def handle_solution(f, problem_id, user, lang):
	_, end = f.name.split('.')
	with open('/home/campovski/{0}_{1}.{2}'.format(problem_id, user, end), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
