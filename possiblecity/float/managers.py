# float/managers.py

import datetime

from django.db import models
from django.db.models.query import QuerySet

class ProjectMixin(object):
    def live(self):
        return self.get_query_set().filter(status=self.model.STATUS_LIVE,
            published__lte=datetime.datetime.now())

class ProjectQuerySet(QuerySet, ProjectMixin):
    pass

class ProjectManager(models.Manager, PostMixin):
    def get_query_set(self):
        return ProjectQuerySet(self.model, using=self._db)