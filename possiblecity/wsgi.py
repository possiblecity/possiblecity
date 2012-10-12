"""
WSGI config for possiblecity project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands 
discover this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it 
also might make sense to replace the whole Django WSGI application with a 
custom one that later delegates to the Django one. For example, you could 
introduce WSGI middleware here, or combine a Django application with an 
application of another framework.

"""
import os
import site
import sys

site.addsitedir('/home/dmeehan/.virtualenvs/prod/lib/python2.7/site-packages')
project = '/home/dmeehan/thepossiblecity.com/production/possiblecity/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE'] = 'possiblecity.settings'
application = WSGIHandler()

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
