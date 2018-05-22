from django.core.exceptions import ObjectDoesNotExist
from signup.models import User


"""
	Check if user has supplied correct (username, password) combination
	and if user has activated his account.
	@param user: username or email
	@param pwd: password
	@return username or None if wrong credentials.
"""
def validate_login(user, pwd):
	try:
		if '@' in user: # is email
			user = User.objects.get(email=user, password=pwd)
		else: # is username
			user = User.objects.get(username=user, password=pwd)
		if user and user.is_active:
			return user.username
	except ObjectDoesNotExist:
		return None
