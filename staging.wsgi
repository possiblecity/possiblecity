#!/usr/bin/python
import os, site, sys


# Tell wsgi to add the Python site-packages to it's path.
site.addsitedir('/home/futuregreen/.virtualenvs/staging/lib/python2.7/site-packages')

# Fix markdown.py (and potentially others) using stdout
sys.stdout = sys.stderr

root = os.path.dirname(__file__)
project = os.path.join(root, 'futuregreen')
workspace = os.path.dirname(project)
sys.path.append(workspace)

os.environ['DJANGO_SETTINGS_MODULE'] = 'futuregreen.settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()