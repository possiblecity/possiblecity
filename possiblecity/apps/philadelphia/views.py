# philadelphia/views.py

from rest_framework import viewsets

from .models import Neighborhood

from .serializers import NeighborhoodSerializer

class NeighborhoodApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Neighborhoods to be consumed as geojson.
    """
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer
    paginate_by = None
