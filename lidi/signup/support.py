from django.core.mail import send_mail
from .models import User
import os
import hashlib
import random

def generate_random_link(username):
	hashed = hashlib.sha256(b'{0}'.format(username)).hexdigest()
	for _ in range(40):
		hashed += str(random.randint(0, 9))
	return 'http://127.0.0.1:8000/signup/confirm/{0}'.format(hashed)

def add_tmp_user(username, password, email, country, language, programming_language):
	user = User()
	user.username = username
	user.password = password
	user.email = email
	user.country_id = country.id
	user.language_id = language.id
	user.programming_language_id = programming_language.id

	link = generate_random_link(username)
	user.conf_link = link

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
