# lotxlot/models.py

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models import permalink

from taggit.managers import TaggableManager

class Lot(models.Model):
    pass

    zip_code =
    location =
    owner =
    bldg_code =
    area =
    is_vacant = models.BooleanField(default=False)

    steward = models.ManyToManyFied(User, blank=True, null=True)


class LotImage(models.Model):
    pass