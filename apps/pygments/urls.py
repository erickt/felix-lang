from django.conf.urls.defaults import *

urlpatterns = patterns('apps.pygments.views',
    (r'^style\.css$', 'style'),
)
