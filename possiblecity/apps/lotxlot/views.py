# lotxlot/views.py
from django.contrib.gis.geos import Polygon
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormView


from rest_framework import viewsets, filters
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer, JSONPRenderer
from rest_framework.serializers import ModelSerializer
from rest_framework_gis.filters import InBBOXFilter

from apps.ideas.forms import SimpleIdeaForm
from apps.ideas.models import Idea

from .models import Lot
from .utils import fetch_json

from .serializers import LotSerializer, LotPointSerializer

########## Mixins ##########

class BBoxMixin(object):
    def get_queryset(self):
        queryset = super(BBoxMixin, self).get_queryset()
        bbox = self.request.QUERY_PARAMS.get('bbox', None)
        if bbox:
            try:
                p1x, p1y, p2x, p2y = (float(n) for n in bbox.split(','))
            except ValueError:
                raise APIException("Not valid bbox string in parameter %s."
                               % bbox)

            poly = Polygon.from_bbox((p1x, p1y, p2x, p2y))
            queryset = queryset.filter(coord__contained=poly)
        return queryset

########## HTML Views ##########
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


class LotIndexView(TemplateView):
    template_name='lotxlot/map.html'


########## API Views ##########


class LotApiViewSet(BBoxMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Lots to be consumed as geojson
    """
    queryset = Lot.objects.filter(is_vacant=True).filter(is_visible=True).prefetch_related('idea_set')
    serializer_class = LotSerializer
    renderer_classes = (JSONRenderer, JSONPRenderer)
    filters = (InBBOXFilter,)
    paginate_by = None

class PublicLotApiViewSet(LotApiViewSet):
    queryset = Lot.objects.filter(
           is_vacant=True).filter(
           is_visible=True).filter(
           is_public=True).prefetch_related('idea_set')

class PrivateLotApiViewSet(LotApiViewSet):
    queryset = Lot.objects.filter(
           is_vacant=True).filter(
           is_visible=True).filter(
           is_public=False).prefetch_related('idea_set')

class LotPointApiViewSet(LotApiViewSet):
    serializer_class = LotPointSerializer
    
    
class LotIdeaApiViewSet(BBoxMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Lots with Ideas to be consumed as geojson.
    """
    queryset = Lot.objects.filter(idea__isnull=False).prefetch_related('idea_set')
    serializer_class = LotPointSerializer
    
    paginate_by = None




