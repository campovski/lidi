from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Problem, Submission
from signup.models import User
from .forms import UploadSolutionForm
from .support import handle_solution, get_solutions_and_times

def index(request, page=1, sort_by='id'):
	all_problems = Problem.objects.all().order_by(sort_by)

	if not all_problems:
		return HttpResponse("Empty db")
	
	try:
		request.session['user']
	except KeyError:
		request.session['user'] = None

	if page == 0:
		return render(request, 'problem/index.html', { 'problems': all_problems, 'user': request.session['user'] })

	paginator = Paginator(all_problems, 100)
	try:
		problems = paginator.page(page)
	except PageNotAnInteger:
		problems = paginator.page(1)
	except EmptyPage:
		problems = paginator.page(paginator.num_pages)
	
	return render(request, 'problem/index.html', { 'problems': problems, 'user': request.session['user'] })

def detail(request, problem_id=2):
	problem = Problem.objects.filter(pk=problem_id)[0]

	l_grade = -1
	h_grade = -1
	out_time = -1

	try:
		user_id = User.objects.get(username=request.session['user']).id
		submission = Submission.objects.get(user=user_id, problem=problem_id)
		h_grade = submission.grade
		out_time = get_solutions_and_times(request.session['user'], problem_id)
	except KeyError:
		request.session['user'] = None
	except ObjectDoesNotExist:
		pass

	if request.method == 'POST':
		form = UploadSolutionForm(request.POST, request.FILES)
		if form.is_valid():
			if request.session['user'] != None:
				l_grade, h_grade, error = handle_solution(request.FILES['f'], problem_id, request.session['user'], form.cleaned_data['prog_lang'].name.strip())
				out_time = get_solutions_and_times(request.session['user'], problem_id)
				return render(request, 'problem/detail.html', { 'problem': problem, 'form': form, 'user': request.session['user'], 'grade': h_grade, 'l_grade': l_grade, 'error': error, 'out_time': out_time })
			else:
				return HttpResponse("Please login")
	else:
		form = UploadSolutionForm()
	return render(request, 'problem/detail.html', { 'problem': problem, 'form': form, 'user': request.session['user'], 'grade': h_grade, 'l_grade': l_grade, 'error': -1, 'out_time': out_time })
