import os

from lidi.settings import FILETYPES, MAX_UPLOAD_SIZE


def handle_uploaded_file(f):
    """
        Saves uploaded problem files to temporary directory where they will be reviewed.
        :param f: uploaded file
        :returns 0 if limits are not satisfied, 1 if everything is OK
    """

    if not limits_ok(f):
        return 0
    directory = os.popen('echo $CG_FILES_PROBLEMS_TMP').read().strip()
    with open('{0}/{1}'.format(directory, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return 1


def limits_ok(f):
    """
        Checks if uploaded file satisfies limits set.
        :param f: uploaded file
        :returns 1 if limits are satisfied, otherwise 0
    """

    ending = f.name.split('.')[-1]
    if ending not in FILETYPES or f._size > MAX_UPLOAD_SIZE:
        return 0
    return 1
