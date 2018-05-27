import os
import subprocess
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
        pass  # directory already exists

    # Write the submission file to previously created directory, rename it.
    _, end = f.name.split('.')
    f_local = '{2}_{0}.{1}'.format(user, end, problem_id)
    with open('{0}/{1}'.format(problem_dir, f_local), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Grade the task using agrader.sh. First compile the program if necessary and then copy
    # files to docker container. Then run the program and check the grade
    # with grader.
    runner_ret_val = -1
    grade = -1
    error = -1
    compiler_output = \
        subprocess.check_output('bash problem/grader/compile_and_copy.sh {0} {1} {2}'.format(f_local, problem_id, user),
                                shell=True).split('\n')[-2]
    if compiler_output == 'OK':
        if end == 'py':
            if lang == 'Python 2':
                runner_ret_val = subprocess.call('bash problem/grader/run_py.sh {0} {1}'.format(user, problem_id),
                                                 shell=True)
            elif lang == 'Python 3':
                runner_ret_val = subprocess.call('bash problem/grader/run_py3.sh {0} {1}'.format(user, problem_id),
                                                 shell=True)
        elif end == 'java':
            runner_ret_val = subprocess.call('bash problem/grader/run_java.sh {0} {1}'.format(user, problem_id),
                                             shell=True)
        elif end == 'cs':
            runner_ret_val = subprocess.call('bash problem/grader/run_cs.sh {0} {1}'.format(user, problem_id),
                                             shell=True)
        else:
            runner_ret_val = subprocess.call('bash problem/grader/run_c.sh {0} {1}'.format(user, problem_id), shell=True)

        if runner_ret_val == 0:
            grader_out = subprocess.check_output('bash problem/grader/grade.sh {0} {1}'.format(user, problem_id),
                                                 shell=True).split('\n')[-2]
            try:
                grade = int(grader_out)
            except ValueError:
                grade = -1
                error = grader_out
        else:
            error = "RTE"

    else:
        error = compiler_output

    # Add submission
    user = User.objects.get(username=user)
    today = date.today()
    today_str = '{0}-{1}-{2}'.format(today.year, today.month, today.day)
    try:  # if user has already submitted solution for this problem before
        submission = Submission.objects.get(user=user.id, problem=problem_id)
        submission.tries += 1
        if grade > submission.grade:
            submission.grade = grade
            submission.date = today_str

        # Save newer solution with same points.
        if grade >= submission.grade:
            os.system('bash problem/grader/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 1))
        else:
            os.system('bash problem/grader/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 0))

    except ObjectDoesNotExist:  # this is user's first submission
        submission = Submission()
        submission.user_id = user.id
        submission.problem_id = problem_id
        submission.grade = grade
        submission.date = today_str
        submission.tries = 1
        os.system('bash problem/grader/move_output.sh {0} {1} {2}'.format(user.username, problem_id, 1))

    finally:  # at the end we need to update some data about best submissions
        if grade == 10 and submission.tries_until_correct == 0:
            submission.tries_until_correct = submission.tries

            # Update number of people that solved this problem.
            problem = Problem.objects.get(pk=problem_id)
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
        :return: data about submissions
    """
    problem_dir = '{0}/{1}/{2}'.format(os.popen('echo $CG_FILES_UPLOADED').read().strip(), username, problem_id)

    last_outputs = get_last_outputs(problem_dir, problem_id, username)
    best_outputs = get_best_outputs(problem_dir, problem_id, username)
    last_times = get_times('{}/last_out/time'.format(problem_dir))
    best_times = get_times('{}/best_out/time'.format(problem_dir))
    program = get_program('{}/prog/'.format(problem_dir))

    last_outs = zip(last_outputs, last_times) if last_outputs != -1 or last_times != -1 else -1
    best_outs = zip(best_outputs, best_times) if best_outputs != -1 or best_times != -1 else -1

    return last_outs, best_outs, program


def get_last_outputs(problem_dir, problem, user):
    """
        Gets outputs of last submission.
        :param problem_dir: main directory of submissions
        :param problem: id of problem
        :param user: user who wants to see submission for problem
        :return: -1 if no file found, otherwise array of last outputs
    """

    outputs = []
    try:
        for i in range(10):
            outputs.append([])
            f = open('{0}/last_out/out_{1}_{2}_{3}'.format(problem_dir, problem, user, i))
            for line in f:
                outputs[i].append(line.strip())
            f.close()
    except IOError:
        return -1
    return outputs


def get_best_outputs(problem_dir, problem, user):
    """
        Gets outputs of best submission.
        :param problem_dir: main directory of submissions
        :param problem: id of problem
        :param user: user who wants to see submission for problem
        :return: -1 if no file found, otherwise array of best outputs
    """

    outputs = []
    try:
        for i in range(10):
            outputs.append([])
            f = open('{0}/best_out/out_{1}_{2}_{3}'.format(problem_dir, problem, user, i))
            for line in f:
                outputs[i].append(line.strip())
            f.close()
    except IOError:
        return -1
    return outputs


def get_times(f_times):
    """
        Gets times from f_times.
        :param f_times: file path of times
        :return: -1 if no file found, otherwise array of times
    """

    times = []
    try:
        f = open(f_times)
        for line in f:
            line = int(line)
            if line > 10000:
                line_transformed = '{0}.{1}s'.format(line/10000, (line/1000) % 10)
            elif line > 1000:
                line_transformed = '{}ms'.format(line/1000)
            else:
                line_transformed = '{0}.{1}ms'.format(line/10, line % 10)
            times.append(line_transformed)
        f.close()
    except IOError:
        return -1
    return times


def get_program(dir_program):
    """
        Finds the program and gets it.
        :param dir_program: directory where the program is
        :return:
    """

    f_program = os.path.join(dir_program, os.popen('ls {}'.format(dir_program)).read().strip())
    program = ""
    try:
        f = open(f_program)
        for line in f:
            program += line
        f.close()
    except IOError:
        return -1
    return program.replace('\t', ' '*4)
