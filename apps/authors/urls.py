from django.conf.urls.defaults import *
from django.contrib.auth.models import User

info_dict = {
    'queryset': User.objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
   (r'^$', 'object_list', dict(info_dict, allow_empty=True, template_name='authors/author_list.html')),
)

urlpatterns += patterns('apps.authors.views',
    (r'^(?P<username>[\w-]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'authors_day'),
    (r'^(?P<username>[\w-]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'authors_month'),
    (r'^(?P<username>[\w-]+)/$', 'authors_index'),
)
