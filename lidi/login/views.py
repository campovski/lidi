from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import LoginForm, PasswordResetEmailForm, PasswordResetChangePasswordForm
from .support import validate_login, send_reset_password, validate_reset_link, reset_pwd
from lidi.settings import BASE_HTTP_ADDRESS


def index(request, error=None):
    """
        Load login page.
        :param request
        :param error: denotes if there was some wrong try while trying to log in
    """

    # If user is already logged in, we do not need to log him in.
    try:
        if request.session['user'] is not None:
            return redirect(BASE_HTTP_ADDRESS)
    except KeyError:
        pass  # continue with logging in

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
                return render(request, 'login/index.html', {'form': form, 'valid': False, 'error': error})
    else:
        form = LoginForm()

    return render(request, 'login/index.html', {'form': form, 'valid': True, 'error': error})


def logout(request):
    """
        Logs user out just by setting current user to None.
        :param request
    """

    request.session['user'] = None
    return redirect(BASE_HTTP_ADDRESS)


def reset_password(request, conf_link=None):
    """
        If conf_link is None, serve page where user can reset password.
        If conf_link is set, provide the possibility to enter new password.
        :param request
        :param conf_link: if present, user has clicked the link, else default page
    """

    # User has to enter email or username.
    if conf_link is None:
        if request.method == 'POST':
            form = PasswordResetEmailForm(request.POST)
            if form.is_valid():
                if send_reset_password(form.cleaned_data['user']):
                    return HttpResponse('Check your email for password reset link')
                else:
                    return HttpResponse('Oops, something went wrong, please try again')
        else:
            form = PasswordResetEmailForm()
        return render(request, 'login/reset_index.html', {'form': form})

    # User has clicked on a reset password link in email.
    if validate_reset_link(conf_link):
        if request.method == 'POST':
            form = PasswordResetChangePasswordForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                    if reset_pwd(form.cleaned_data['username'], form.cleaned_data['password1'], conf_link):
                        return HttpResponse('Password has been reset')
                    else:
                        return render(request, 'login/reset_index.html', {'form': form, 'error': 2})
                else:
                    return render(request, 'login/reset_index.html', {'form': form, 'error': 1})
        else:
            form = PasswordResetChangePasswordForm()
        return render(request, 'login/reset_index.html', {'form': form, 'error': 0})

    # Wrong conf_link.
    return HttpResponse('Wrong reset password link')
