from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm
from .support import add_tmp_user
from lidi.settings import BASE_HTTP_ADDRESS

def index(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
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
	return render(request, 'signup/index.html', { 'form': form })
