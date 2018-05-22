SECRET_KEY = 'vsdjhv093rvo32l2mlfk32l2VJsvormkm'

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'lidi_db',
      'USER': 'admin_lidi',
      'PASSWORD': 'testpwd1',
      'HOST': 'localhost',
      'PORT': ''
    }
}

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''

GOOGLE_RECAPTCHA_SECRET_KEY = ''
