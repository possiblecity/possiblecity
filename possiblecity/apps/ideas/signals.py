import django.dispatch


idea_created = django.dispatch.Signal(providing_args=["idea", "request"])
idea_updated = django.dispatch.Signal(providing_args=["idea", "request"])