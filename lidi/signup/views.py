from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import User
from .forms import SignupForm
from .support import add_tmp_user, confirm_user, validate_recaptcha
from lidi.settings import BASE_HTTP_ADDRESS


"""
	Load signup page.
"""
def index(request):
	# If user wants to signup but is already signed in, log previous user out.
	try:
		if request.session['user'] is not None:
			return redirect('login:logout')
	except KeyError:
		request.session['user'] = None

	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			if not validate_recaptcha(request):
				return redirect('signup:index', permanent=True)

			user = form.cleaned_data['username']
			pwd = form.cleaned_data['password']
			repwd = form.cleaned_data['repeat_password']
			email = form.cleaned_data['email']
			country = form.cleaned_data['country']
			language = form.cleaned_data['language']
			programming_language = form.cleaned_data['programming_language']
			if pwd == repwd:
				add_tmp_user(user, pwd, email, country, language, programming_language)
				return redirect(BASE_HTTP_ADDRESS)
	else:
		form = SignupForm()
		
	return render(request, 'signup/index.html', { 'form': form, 'user': request.session['user'] })


"""
	Loads the page with results of confirming the user, when user clicked
	on confirmation link.
	@param conf_link: confirmation sequence
"""
def confirm(request, conf_link):
	ret_val = confirm_user(conf_link)
	if ret_val == 0:
		return HttpResponse('Your account has been activated')
	elif ret_val == -1:
		return HttpResponse('Hm, that\'s strange...')
	elif ret_val == -2:
		return HttpResponse('Your link appears to be broken...')
	elif ret_val > 0:
		return HttpResponse('Oops, we could not make you a directory.')
	return HttpResponse('You should not even get here...')
