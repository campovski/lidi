from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .forms import UploadFileForm
from .support import handle_uploaded_file

def upload_file(request):
	try:
		request.session['user']
	except KeyError:
		request.session['user'] = None	

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['f'])
			return HttpResponse("File uploaded is {0}".format(request.FILES['f']))
	else:
		form = UploadFileForm()
	return render(request, 'upload/upload.html', { 'form': form, 'user': request.session['user'] })

