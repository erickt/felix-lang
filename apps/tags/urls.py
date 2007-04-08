from django.conf.urls.defaults import *
from models import Tag

info_dict = {
    'queryset': Tag.objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
   (r'^$', 'object_list', dict(info_dict, allow_empty=True)),
)

urlpatterns += patterns('apps.tags.views',
    (r'^create/$', 'add_edit_tag'),
    (r'^(?P<slug>[\w-]+)/update/$', 'add_edit_tag'),
    (r'^(?P<slug>[\w-]+)/delete/$', 'delete_tag'),
    (r'^(?P<slug>[\w-]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'tags_day'),
    (r'^(?P<slug>[\w-]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'tags_month'),
    (r'^(?P<slug>[\w-]+)/$', 'tags_index'),
)
