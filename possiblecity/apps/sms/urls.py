# sms/urls.py
from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^$', 'apps.sms.views.process_sms', name='sms_process_sms'),
)