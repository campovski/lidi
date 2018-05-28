from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from signup.models import User
from signup.support import generate_random_seq
from lidi.settings import BASE_HTTP_ADDRESS


def validate_login(user, pwd):
    """
        Check if user has supplied correct (username, password) combination
        and if user has activated his account.
        :param user: username or email
        :param pwd: password
        :return username or None if wrong credentials.
    """

    try:
        if '@' in user:  # is email
            user = User.objects.get(email=user, password=pwd)
        else:  # is username
            user = User.objects.get(username=user, password=pwd)
        if user and user.is_active:
            return user.username
    except ObjectDoesNotExist:
        return None


def send_reset_password(user):
    """
        Sends email to user for password reset.
        :param user: user who wants to reset password, either email or username
        :return: 1 if success, 0 if not
    """

    try:
        if '@' in user:  # is email
            user = User.objects.get(email=user)
        else:  # is username
            user = User.objects.get(username=user)

        if user and user.is_active:
            # Generate confirmation sequence and save it to user.
            seq = generate_random_seq()
            user.conf_link = seq

            # Send mail.
            link = '{0}/login/reset_password/{1}'.format(BASE_HTTP_ADDRESS, seq)
            subject = '[codegasm] Reset Your Password'
            msg = 'Please click on the following link to reset your password\n\n {0}'.format(link)
            fro = 'campovski@gmail.com'
            to = [user.email]
            send_mail(subject, msg, fro, to, fail_silently=False)

            user.save()
            return 1
    except User.DoesNotExist:
        return 1


def validate_reset_link(conf_link):
    """
        Checks if a reset link exists in database.
        :param conf_link: confirmation sequence
        :return: 1 if exists, otherwise 0
    """
    try:
        User.objects.get(conf_link=conf_link)
        return 1
    except User.DoesNotExist:
        return 0


def reset_pwd(username, password, conf_link):
    """
        Checks if username matches the confirmation link. If so, it resets the password.
        :param username: username of user to reset password of
        :param password: user's new password
        :param conf_link: confirmation sequence to check if it matches with username
        :return: 1 if successful (username, conf_link) pair OK, otherwise 0
    """

    try:
        user = User.objects.get(username=username, conf_link=conf_link)
        user.password = password
        user.save()
        return 1
    except User.DoesNotExist:
        return 0
