# ideas/managers.py

import datetime

from django.db import models
from django.db.models.query import QuerySet

class IdeaQuerySet(QuerySet):
    def published(self):
        return self.filter(status=self.model.STATUS_PUBLISHED)

