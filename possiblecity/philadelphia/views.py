import json

request
geojson
HttpResponse
render_to_response

from possiblecity.philadelphia.models import Lot

def lots(request):
    lots = Lots.objects.all()
    bbox = json.dumps(lots.extent())
    if request.is_ajax():
       d = {}
       for lot inlots.geojson():
            geojson = json.loads(lots.geojson)
            d[county.geo_id] = geojson
        return HttpResponse(json.dumps(d), mimetype='application/json')
    else:
        return render_to_responsel'lots.html', { 'bbox': bbox }, context_instance=RequestContext(request))
