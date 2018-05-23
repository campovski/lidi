from django.shortcuts import render


def index(request):
    try:
        return render(request, 'home/index.html', {'user': request.session['user']})
    except KeyError:
        return render(request, 'home/index.html', {'user': None})
