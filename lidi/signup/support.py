from django.core.mail import send_mail
from .models import User
from lidi.settings import BASE_HTPP_ADDRESS
import os
import hashlib
import random

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

def user_confirmed(user):
	usr = User.objects.get(username=user)
	usr.is_active = True
	usr.save()

	# Safety precautions
	usr = User.objects.get(username=user)
	if usr.is_active:
		return os.system('mkdir $CG_FILES_UPLOADED/{0}'.format(usr.username))
	return -1
