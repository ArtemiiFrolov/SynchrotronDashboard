from .base import *

DEBUG = True
SECRET_KEY = 'h5m@*ihiz#yo+dri&2w^eo%9)cz%kn=f*dp4__g9urkwkeu1)+'
STATIC_ROOT = './static/'
MEDIA_ROOT = './media/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
