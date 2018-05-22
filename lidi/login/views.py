from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import LoginForm
from .support import validate_login
from lidi.settings import BASE_HTTP_ADDRESS


"""
	Load login page.
	@param error: denotes if there was some wrong try while trying to log in
"""
def index(request, error=None):
	# If user is already logged in, we do not need to log him in.
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

"""
	Logs user out just by setting current user to None.
"""
def logout(request):
	request.session['user'] = None
	return redirect(BASE_HTTP_ADDRESS)
