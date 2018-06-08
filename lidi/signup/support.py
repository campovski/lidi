import os
import random
import urllib
import urllib2
import json

from django.core.mail import send_mail

from .models import User
from statistics.models import Rating
from lidi.settings import BASE_HTTP_ADDRESS
from lidi.local_settings import GOOGLE_RECAPTCHA_SECRET_KEY


def generate_random_seq():
    """
        Generates random sequence that will be used in activation link in mail.
    """

    hashed = ''
    while len(hashed) < 61:
        hashed += str(random.randint(0, 9))
    return hashed


def add_tmp_user(username, password, email, country, language, programming_language):
    """
        Adds user to database, but does not activate his account.
        :param username
        :param password
        :param email
        :param country
        :param language
        :param programming_language
    """

    # Fill in data we got.
    user = User()
    user.username = username
    user.password = password
    user.email = email
    user.country_id = country.id
    user.language_id = language.id
    user.programming_language_id = programming_language.id

    # Generate activation sequence and save it to user.
    seq = generate_random_seq()
    user.conf_link = seq

    # Send mail.
    link = '{0}/signup/confirm/{1}'.format(BASE_HTTP_ADDRESS, seq)
    subject = '[codegasm] Confirm your email address'
    msg = 'Please click on the following link to confirm your email address\
        and start using Codegasm.\n\n {0}'.format(link)
    fro = 'campovski@gmail.com'
    to = [email]
    send_mail(subject, msg, fro, to, fail_silently=False)

    user.save()


def confirm_user(conf_link):
    """
        Activate user by confirmation link.
        :param conf_link: confirmation sequence
        :return -2 if such confirmation sequence was not found, error code if we could not create
            directories for user, 0 if all ok
    """

    usr = User.objects.get(conf_link=conf_link)
    if not usr:
        return -2

    create_dir_ret_val = os.system('mkdir $CG_FILES_UPLOADED/{0}'.format(usr.username))
    if create_dir_ret_val != 0:
        return create_dir_ret_val

    usr.is_active = True
    usr.conf_link = ''

    # Create docker container for user.
    container_id = os.popen('docker create -it --name lidi_container_{} --network none ubuntu:lidi'.format(usr.username)).read()
    usr.container_id = container_id[:12]
    usr.save()

    # Initialize his rating.
    rating = Rating()
    rating.user = usr
    rating.save()

    return 0


def validate_recaptcha(request):
    """
        Creates POST request to Google's recaptcha service in order to check
        if user passed recaptcha test.
        :param request
        :return result of test
    """

    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = json.load(response)
    return result['success']

