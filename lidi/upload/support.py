from lidi.settings import FILETYPES, MAX_UPLOAD_SIZE
import os

def handle_uploaded_file(f):
	if not limits_ok(f):
		return 0
	directory = os.popen('echo $CG_FILES_PROBLEMS_TMP').read().strip()
	with open('{0}/{1}'.format(directory, f.name), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return 1

def limits_ok(f):
	ending = f.name.split('.')[-1]
	if ending not in FILETYPES or f._size > MAX_UPLOAD_SIZE:
		return 0
	return 1
