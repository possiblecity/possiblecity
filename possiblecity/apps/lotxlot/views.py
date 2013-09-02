# lotxlot/views.py
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormView


from rest_framework import viewsets

from apps.ideas.forms import SimpleIdeaForm
from apps.ideas.models import Idea

from .models import Lot
from .utils import fetch_json

from .serializers import LotSerializer



class LotDisplay(DetailView):
    model = Lot

    def get_context_data(self, **kwargs):
        context = super(LotDisplay, self).get_context_data(**kwargs)
        context['form'] = SimpleIdeaForm()
        return context

class LotAddIdeaView(FormView, SingleObjectMixin):
    model=Lot
    form_class = SimpleIdeaForm
    template_name = 'lotxlot/lot_detail.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.session['post'] = request.POST
            url = "%s?next=%s" % (reverse('account_login'), request.path)
            return HttpResponseRedirect(url)
        else:
            self.object = self.get_object()
            return super(LotAddIdeaView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('lotxlot_lot_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        Auto-populate user
        and save form.
        """
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        instance.lots.add(self.object)
        instance.save()

        return HttpResponseRedirect(self.get_success_url())

class LotDetailView(View):
    def get(self, request, *args, **kwargs):
        view = LotDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = LotAddIdeaView.as_view()
        return view(request, *args, **kwargs)



# api views

class LotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Lots to be viewed or edited.
    """
    queryset = Lot.objects.filter(is_vacant=True).filter(is_visible=True)
    serializer_class = LotSerializer
    paginate_by = None







