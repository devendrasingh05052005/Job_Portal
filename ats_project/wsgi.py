# ats_project/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Whitenoise is now configured in settings.py MIDDLEWARE
# Isliye ab is import ki zaroorat nahi hai.
# from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats_project.settings')

application = get_wsgi_application()

# Whitenoise is configured in middleware, so this line is not needed
# application = DjangoWhiteNoise(application)