# philadelphia/views.py

from rest_framework import viewsets

from .models import Neighborhood

from .serializers import NeighborhoodSerializer

class NeighborhoodApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Neighborhoods to be consumed as geojson.
    """
    queryset = Neighborhood.objects.filter(
                   name__in=['POINT_BREEZE', 'TIOGA', 'NICETOWN', 
                             'UPPER_KENSINGTON', 'EAST_KENSINGTON',
                             'WEST_KENSINGTON', 'OLD KENSINGTON',
                             'FAIRHILL', 'MCGUIRE', 'STRAWBERRY_MANSION',
                             'HARROWGATE', 'BREWERYTOWN', 'HUNTING_PARK' ])
    serializer_class = NeighborhoodSerializer
    paginate_by = None
