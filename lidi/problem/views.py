from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, Http404

from .models import Problem, Submission
from signup.models import User
from .forms import UploadSolutionForm
from .support import handle_solution, get_solutions_and_times


def index(request, page=1, sort_by='id'):
    """
        Loads a page with the list of problems. It supports pagination.
        :param request
        :param page: page of pagination of problems
        :param sort_by: what column do we want to sort by
    """

    # Get all problems.
    all_problems = Problem.objects.all().order_by(sort_by)

    # If there are none, return basic HttpResponse.
    if not all_problems:
        return HttpResponse("Empty db")

    # Check if user variable is stored in session. If not, set the variable to None.
    try:
        request.session['user']
    except KeyError:
        request.session['user'] = None

    # View all problems at once, without pagination.
    if page == 0:
        return render(request, 'problem/index.html', {'problems': all_problems, 'user': request.session['user']})

    paginator = Paginator(all_problems, 1)
    try:  # return the proper page
        problems = paginator.page(page)
    except PageNotAnInteger:
        problems = paginator.page(1)
    except EmptyPage:  # if page is out of range, return the last page
        return redirect('problem:index', page=paginator.num_pages, sort_by=sort_by)

    return render(request, 'problem/index.html', {'problems': problems, 'user': request.session['user']})


def detail(request, problem_id):
    """
        Loads a page with details of desired problem.
        :param request
        :param problem_id: id of problem user want to see details for
    """

    # Get the details of problem. If problem with id problem_id does not exist, raise 404.
    try:
        problem = Problem.objects.get(pk=problem_id)
    except Problem.DoesNotExist:
        raise Http404("Problem with given id does not exist.")

    l_grade = -1
    h_grade = -1
    out_time = -1

    # Get possible data about user's previous submissions.
    try:
        user_id = User.objects.get(username=request.session['user']).id
        submission = Submission.objects.get(user=user_id, problem=problem_id)
        h_grade = submission.grade
        out_time = get_solutions_and_times(request.session['user'], problem_id)
    except KeyError:  # user is not logged in
        request.session['user'] = None
    except ObjectDoesNotExist:  # if no submissions, do nothing
        pass

    # If user submitted the program, we need to handle that.
    if request.method == 'POST':
        form = UploadSolutionForm(request.POST, request.FILES)
        if form.is_valid():
            if request.session['user'] is not None:
                l_grade, h_grade, error = handle_solution(request.FILES['f'], problem_id, request.session['user'], \
                                                          form.cleaned_data['prog_lang'].name.strip())
                out_time = get_solutions_and_times(request.session['user'], problem_id)
                return render(request, 'problem/detail.html', {'problem': problem, 'form': form, 'user': request.session['user'], \
                                                               'grade': h_grade, 'l_grade': l_grade, 'error': error, \
                                                               'out_time': out_time})
            else:
                return HttpResponse("Please login")
    else:
        form = UploadSolutionForm()

    return render(request, 'problem/detail.html', {'problem': problem, 'form': form, 'user': request.session['user'], \
                                                   'grade': h_grade, 'l_grade': l_grade, 'error': -1, \
                                                   'out_time': out_time})

