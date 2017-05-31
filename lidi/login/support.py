from signup.models import User

def validate_login(user, pwd):
	if '@' in user:
		user = User.objects.filter(email=user, password=pwd)
	else:
		user = User.objects.filter(username=user, password=pwd)
	if user and user[0].is_active:
		return user[0].username
	return None
