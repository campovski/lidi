from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from .support import validate_login
from lidi.settings import BASE_HTTP_ADDRESS

def index(request, error=None):
	try:
		if request.session['user'] is not None:
			return redirect(BASE_HTTP_ADDRESS)
	except KeyError:
		pass # continue with logging in

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
				return render(request, 'login/index.html', { 'form': form, 'valid': False, 'error': error })
	else:
		form = LoginForm()
	return render(request, 'login/index.html', { 'form': form, 'valid': True, 'error': error })

def logout(request):
	request.session['user'] = None
	return redirect(BASE_HTTP_ADDRESS)
