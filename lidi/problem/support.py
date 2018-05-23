import os
import re
from datetime import date

from django.core.exceptions import ObjectDoesNotExist

from signup.models import User
from problem.models import Problem
from .models import Submission


def handle_solution(f, problem_id, user, lang):
    """
        When user uploads the solution, this function takes care of it.
        It runs the grader, saves the running time and output and saves
        the submission info to database.
        :param f: submission file (program)
        :param problem_id: the id of the problem user submitted solution to
        :param user: user id of user that made submission
        :param lang: what language did user use
        :return grade: grade that user got in this submission
        :return submission.grade: best grade user got on this problem
        :return error: -1 if no errors, otherwise output of agrader.sh
    """

    # Get directory where files are stored.
    directory = os.popen('echo $CG_FILES_UPLOADED').read().strip()

    # Create directory where user's problem submission stuff will get stored.
    problem_dir = "{0}/{1}/{2}".format(directory, user, problem_id)
    try:
        os.mkdir(problem_dir)
    except OSError:
        pass # directory already exists

    # Write the submission file to previously created directory, rename it.
    _, end = f.name.split('.')
    f_local = '{2}_{0}.{1}'.format(user, end, problem_id)
    with open('{0}/{1}'.format(problem_dir, f_local), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Grade the task using agrader.sh
    grader_out = os.popen('bash problem/bash/agrader.sh {0} {1}'.format(f_local, lang)).read()
    error = -1
    try:
        # Get grade. In some proglangs, the grader might print compiler stuff, etc., so we
        # only need the last line, where the grade is.
        grade = int(grader_out.strip().split('\n')[-1])
    except ValueError: # cannot convert to int, meaning the last line is some error
        error = grader_out
        grade = 0
    try:
        rewrite_times('{0}/time'.format(problem_dir))
    except IOError:
        pass # grader quit with error, resulting in not producing the times file

    # Add submission
    user = User.objects.get(username=user)
    today = date.today()
    today_str = '{0}-{1}-{2}'.format(today.year, today.month, today.day)
    try: # if user has already submitted solution for this problem before
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

    except ObjectDoesNotExist: # this is user's first submission
        submission = Submission()
        submission.user_id = user.id
        submission.problem_id = problem_id
        submission.grade = grade
        submission.date = today_str
        submission.tries = 1
        os.system('bash problem/bash/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 1))

    finally: # at the end we need to update some data about best submissions
        if grade == 10 and submission.tries_until_correct == 0:
            submission.tries_until_correct = submission.tries

            # Update number of people that solved this problem.
            problem = Problem.objects.get(problem=problem_id)
            if problem.solved_by_how_many == 0:
                problem.first_solved_by = user
                problem.first_solved_on = today_str
            problem.solved_by_how_many += 1
            problem.last_successful_try = today_str
        submission.save()

    return grade, submission.grade, error


def get_solutions_and_times(username, problem_id):
    """
        Read outputs of last and best submission, the program user submitted and
        running time of last and best submission.
        :param username: username of user whose data we want to get
        :param problem_id: id of problem for which we want to get data
        :return -1 if some IOError occured
        :return output_l: output of last submission
        :return output_h: output of best submission
        :return program: the source code of submission
        :return times: array of running times on testcases of last and best submission
    """

    outputs_l = []  # what last submission outputted
    outputs_h = []  # what best submission outputted

    up_dir = '{0}/{1}/{2}'.format(os.popen('echo $CG_FILES_UPLOADED').read().strip(), username, problem_id)

    try:
        for i in range(10):
            outputs_h.append([])
            f = open('{0}/best_out/out_{1}_{2}_{3}'.format(up_dir, problem_id, username, i))
            for line in f:
                outputs_h[i].append(line.strip())
            f.close()

            outputs_l.append([])
            f = open('{0}/last_out/out_{1}_{2}_{3}'.format(up_dir, problem_id, username, i))
            for line in f:
                outputs_l[i].append(line.strip())
            f.close()

        # Read solution to problem (program).
        prog_name = os.popen('ls {0}/prog'.format(up_dir)).read().strip()
        f = open('{0}/prog/{1}'.format(up_dir, prog_name))
        program = f.readlines()
        f.close()

        # Read times.
        times = [[], []]
        f = open('{0}/last_out/time'.format(up_dir))
        for line in f:
            times[0].append(line.strip())
        f.close()

        f = open('{0}/best_out/time'.format(up_dir))
        for line in f:
            times[1].append(line.strip())
        f.close()

        return outputs_l, outputs_h, program, times

    except IOError:
        return -1


def rewrite_times(f_times):
    """
        Function rewrites the file that stores times. Grader writes there the output
        of unix time function and we need to get the actual time.
        :param f_times: file which we need to rewrite
    """

    f = open(f_times)
    pattern = re.compile(r'(?<=real\t)\d+m\d+.\d\d\ds')
    times = ''
    for line in f:
        tmp = pattern.search(line)
        if tmp is not None:
            times += '{0}\n'.format(tmp.group())
    f.close()

    f = open(f_times, 'w')
    f.write(times)
    f.close()
