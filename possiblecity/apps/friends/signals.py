import django.dispatch


relationship_accepted = django.dispatch.Signal(providing_args=["relationship"])
relationship_declined = django.dispatch.Signal(providing_args=["relationship"])
relationship_removed = django.dispatch.Signal(providing_args=["relationship"])
relationship_created = django.dispatch.Signal(providing_args=["relationship"])
