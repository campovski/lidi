import os

from lidi.settings import FILETYPES, MAX_UPLOAD_SIZE


"""
	Saves uploaded problem files to temporary directory where they will be reviewed.
	@param f: uploaded file
"""
def handle_uploaded_file(f):
	if not limits_ok(f):
		return 0
	directory = os.popen('echo $CG_FILES_PROBLEMS_TMP').read().strip()
	with open('{0}/{1}'.format(directory, f.name), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return 1

"""
	Checks if uploaded file satisfies limits set.
	@param f: uploaded file
"""
def limits_ok(f):
	ending = f.name.split('.')[-1]
	if ending not in FILETYPES or f._size > MAX_UPLOAD_SIZE:
		return 0
	return 1
