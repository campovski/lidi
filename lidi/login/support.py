from django.core.exceptions import ObjectDoesNotExist
from signup.models import User

def validate_login(user, pwd):
	try:
		if '@' in user:
			user = User.objects.get(email=user, password=pwd)
		else:
			user = User.objects.get(username=user, password=pwd)
		if user and user.is_active:
			return user.username
	except ObjectDoesNotExist:
		return None
