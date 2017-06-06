import os
import hashlib
import random
import urllib
import urllib2
import json

from django.core.mail import send_mail

from .models import User

from lidi.settings import BASE_HTTP_ADDRESS
from lidi.local_settings import GOOGLE_RECAPTCHA_SECRET_KEY

def generate_random_seq():
	hashed = ''
	while len(hashed) < 61:
		hashed += str(random.randint(0, 9))
	return hashed

def add_tmp_user(username, password, email, country, language, programming_language):
	user = User()
	user.username = username
	user.password = password
	user.email = email
	user.country_id = country.id
	user.language_id = language.id
	user.programming_language_id = programming_language.id

	seq = generate_random_seq()
	user.conf_link = seq

	link = '{0}/signup/confirm/{1}'.format(BASE_HTTP_ADDRESS, seq)

	subject = '[codegasm] Confirm your email address'
	msg = 'Please click on the following link to confirm your email address\
		and start using Codegasm.\n\n {0}'.format(link)
	fro = 'campovski@gmail.com'
	to = [email]
	send_mail(subject, msg, fro, to, fail_silently=False)

	user.save()

def confirm_user(conf_link):
	usr = User.objects.get(conf_link=conf_link)
	if not usr:
		return -2
	usr.is_active = True
	usr.conf_link = ''
	usr.save()

	return os.system('mkdir $CG_FILES_UPLOADED/{0}'.format(usr.username))

def validate_recaptcha(request):
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