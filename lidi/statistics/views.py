from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
        Load main page of statistics where user can choose category. Also provide
        some basic and most interesting context.
        :param request
    """

    return render(request, 'statistics/index.html')


def problem(request, problem_id=None):
    """
        Loads statistics about problems in general. If problem_id is supplied,
        load statistics about that certain problem.
        :param request
        :param problem_id: id of problem to display statistics about
    """



    return HttpResponse('Statistics problem {}'.format(problem_id))


def country(request, country_slug=None):
    """
        Loads statistics by countries in general. If country_slug is supplied,
        load statistics about that certain country.
        :param request
        :param country_slug: slugified name of country
    """

    return HttpResponse('Statistics country {}'.format(country_slug))


def users(request, username=None):
    """
        Loads statistics about users in general. If username is supplied,
        load statistics about that certain user.
        :param request
        :param username: username to display his detailed stats
    """

    return HttpResponse('Statistics users {}'.format(username))


def achievements(request, achievement_id=None):
    """
        Loads statistics about achievements in general. If achievement_id is supplied,
        load statistics about that certain achievement.
        :param request
        :param achievement_id: id of achievement to display statistics about
    """

    return HttpResponse('Statistics achievements {}'.format(achievement_id))
