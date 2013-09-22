# lotxlot/utils.py
import gc
import json
import md5
import requests

from geopy import geocoders
from urllib import urlencode

from django.config import settings
from django.contrib.gis.geos import Point
from django.core.cache import cache


def geocode_address(address):
    """ returns GeoDjango Point object for given address
    """ 
    g = geocoders.Google()
    try:
        #TODO: not really replace, geocode should use unicode strings
        address = address.encode('ascii', 'replace')            
        text, (lat,lon) = g.geocode(address)
        point = Point(lon,lat)
    except (g.GQueryError):
       raise forms.ValidationError('Please enter a valid address')
    except (g.GeocoderResultError, g.GBadKeyError, g.GTooManyQueriesError):
        raise forms.ValidationError('There was an error geocoding your address. Please try again')
    except:
        raise forms.ValidationError('An unknown error occured. Please try again')

    return point

def fetch_json(url, params, timeout=300):
    """
    Gets data from a REST source and returns a python dictionary.
    If the result is already in cache, it returns cached data.
    Source should be a valid REST url.
    """
    cache_key = url + "?" + urlencode(params)
    m = md5.new()
    cache_key = m.update(cache_key)
    cached = cache.get(cache_key)
    content = ""
    
    if not cached:
        data = requests.get(url, params=params)
        if (data.ok):
            m = md5.new()
            cache_key = m.update(str(data.url))
            cache.set(cache_key, data.text, timeout)
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
		
        if 'features' in dict:
            if dict['features']:
                return True
            else:
            	return False
        else:
            return False

def queryset_iterator(queryset, chunksize=1000):
    '''''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    '''
    pk = queryset.order_by('pk')[0].pk
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()

# convert the projection type of a shapefile
# ogr2ogr -t_srs <New Projection> <Output SHP file> <Original SHP file>
# ogrinfo <Path to SHP file> -al -so
# ogr2ogr -f "ESRI Shapefile" -where "id < 10" new_shapefile.shp huge_shapefile.shp
