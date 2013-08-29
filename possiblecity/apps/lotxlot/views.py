# lotxlot/views.py

from django.core.urlresolvers import reverse
from django.db.models.query import EmptyQuerySet
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponse, HttpResponseRedirect


from extra_views import InlineFormSetView
from rest_framework import viewsets

from apps.ideas.models import Idea

from .models import Lot
from .utils import fetch_json

from .serializers import LotSerializer


class IdeaInlineFormSet(BaseInlineFormSet):
    
    def get_queryset(self):
        return EmptyQuerySet()


class LotDetailView(InlineFormSetView):
    initial = [{'tagline': 'Add your idea for this lot'},]
    model = Lot
    inline_model = Idea
    formset_class = IdeaInlineFormSet
    fields = ('tagline',)
    can_delete = False
    extra = 1
    template_name = 'lotxlot/lot_detail.html'

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            self.request.session['post'] = self.request.POST
            url = "%s?next=%s" % (reverse('account_login'), request.path)
            return HttpResponseRedirect(url)
        else:
            return super(LotDetailView, self).post(request, *args, **kwargs)

    def formset_valid(self, formset):
        """
        Auto-populate user
        and save form.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = self.request.user
            instance.save()

        return HttpResponseRedirect(self.get_success_url())


# api views

class LotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Lots to be viewed or edited.
    """
    queryset = Lot.objects.all()
    serializer_class = LotSerializer







