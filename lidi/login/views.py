from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from .support import validate_login
from lidi.settings import BASE_HTTP_ADDRESS

def index(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data['user']
			pwd = form.cleaned_data['password']
			username = validate_login(user, pwd)
			if username:
				request.session['user'] = username
				return redirect(BASE_HTTP_ADDRESS)
			else:
				return HttpResponse("Wrong username or password")
	else:
		form = LoginForm()
	return render(request, 'login/index.html', { 'form': form })

def logout(request):
	request.session['user'] = None
	return redirect(BASE_HTTP_ADDRESS)
