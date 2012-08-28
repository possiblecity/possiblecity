# lotxlot/utils.py
import json
import requests

from django.core.cache import cache

def fetch_json(source):
    """
    Gets data from a REST source and returns a python dictionary.
    If the result is already in cache, it returns cached data.
    Source should be a valid REST url.
    """

    cached = cache.get(source)
    content = ""
    
    if not cached:
        data = requests.get(source)
        if (data.ok):
            cache.set(source, data.text)
            content = data.text
        else:
            data.raise_for_status()
    else:
        # return cached content
        content = cached
    
    return json.loads(content)    
      

# convert the projection type of a shapefile
# ogr2ogr -t_srs <New Projection> <Output SHP file> <Original SHP file>
# ogrinfo <Path to SHP file> -al -so
# ogr2ogr -f "ESRI Shapefile" -where "id < 10" new_shapefile.shp huge_shapefile.shp
