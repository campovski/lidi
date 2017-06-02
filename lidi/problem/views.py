from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Problem
from .forms import UploadSolutionForm
from .support import handle_solution

def index(request, page=1, sort_by='id'):
	all_problems = Problem.objects.all().order_by(sort_by)

	if not all_problems:
		return HttpResponse("Empty db")
	
	try:
		user = request.session['user']
	except KeyError:
		user = None

	if page == 0:
		return render(request, 'problem/index.html', { 'problems': all_problems, 'user': user })

	paginator = Paginator(all_problems, 100)
	try:
		problems = paginator.page(page)
	except PageNotAnInteger:
		problems = paginator.page(1)
	except EmptyPage:
		problems = paginator.page(paginator.num_pages)
	
	return render(request, 'problem/index.html', { 'problems': problems, 'user': user })

def detail(request, problem_id=2):
	problem = Problem.objects.filter(pk=problem_id)[0]
	
	if request.method == 'POST':
		form = UploadSolutionForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				if request.session['user'] != None:
					grade = handle_solution(request.FILES['f'], problem_id, request.session['user'], "C")
					return HttpResponse("Grade = {0}".format(grade))
				else:
					return HttpResponse("Please login")
			except KeyError:
				return HttpResponse("Please login")
	else:
		form = UploadSolutionForm()
	return render(request, 'problem/detail.html', { 'problem': problem, 'form': form })
