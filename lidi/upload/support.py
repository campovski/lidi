import os

def handle_uploaded_file(f):
	directory = os.popen('echo $CG_FILES_PROBLEMS_TMP').read().strip()
	with open('{0}/{1}'.format(directory, f.name), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
