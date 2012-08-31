# lotxlot/utils.py
import json
import requests
from urllib import urlencode

from django.core.cache import cache

def fetch_json(url, params):
    """
    Gets data from a REST source and returns a python dictionary.
    If the result is already in cache, it returns cached data.
    Source should be a valid REST url.
    """
    cache_key = url + "?" + urlencode(params)
    cached = cache.get(cache_key)
    content = ""
    
    if not cached:
        data = requests.get(url, params=params)
        if (data.ok):
            cache.set(str(data.url), data.text)
            content = data.text
        else:
            data.raise_for_status()
    else:
        # return cached content
        content = cached
    
    return json.loads(content)    
      
def has_feature(url, params):
        """
           Query a Geographic REST service, return True if
           there are any features that match the query 
        """
        dict = fetch_json(url, params)
        if dict["features"]:
            return True
        else:
            return False

# convert the projection type of a shapefile
# ogr2ogr -t_srs <New Projection> <Output SHP file> <Original SHP file>
# ogrinfo <Path to SHP file> -al -so
# ogr2ogr -f "ESRI Shapefile" -where "id < 10" new_shapefile.shp huge_shapefile.shp
