from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError

from .forms import UploadFileForm
from .support import handle_uploaded_file
import login


"""
	Loads a page that provides ability for users to upload their problems.
"""
def upload_file(request):
	# If user is not logged in, set current user to None.
	try:
		request.session['user']
	except KeyError:
		request.session['user'] = None
	
	# If user is not logged in, redirect to login page.
	if request.session['user'] is None:
		return login.views.index(request, 'upload')

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file_ok = handle_uploaded_file(request.FILES['f'])
			request.FILES['f'] = None
			if file_ok:
				return render(request, 'upload/upload.html', { 'form': form, 'user': request.session['user'], 'msg': 1 })
			else:
				return render(request, 'upload/upload.html', { 'form': form, 'user': request.session['user'], 'msg': 0 })
	else:
		form = UploadFileForm()
		
	return render(request, 'upload/upload.html', { 'form': form, 'user': request.session['user'], 'msg': -1 })

