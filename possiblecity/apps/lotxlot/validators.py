# lotxlot/validators.py
from geopy import geocoders
from django.core.exceptions import ValidationError

def validate_address(value):    """ Raise a ValidationError if the value isn't a valid address        or the geocode fails    """
    google = geocoders.Google()    try:
        place, (lat,lng) = google.geocode(data['address'])
    except (GQueryError):
        raise forms.ValidationError('Please enter a valid address')
    except (GeocoderResultError, GBadKeyError, GTooManyQueriesError):
        raise forms.ValidationError('There was an error geocoding your address. Please try again')
    except:
        raise forms.ValidationError('An unknown error occured. Please try again')

