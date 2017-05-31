from .models import User

def add_tmp_user(username, password, email, country, language, programming_language):
	user = User()
	user.username = username
	user.password = password
	user.email = email
	user.country_id = country.id
	user.language_id = language.id
	user.programming_language_id = programming_language.id
	user.save()
