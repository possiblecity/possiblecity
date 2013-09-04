# core/forms.py
from django.db.models.query import EmptyQuerySet
from django.forms.models import BaseInlineFormSet

class EmptyInlineFormSet(BaseInlineFormSet):
    
    def get_queryset(self):
        return EmptyQuerySet()