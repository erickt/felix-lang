from django.conf.urls.defaults import *

from felix_website.apps.blog.models import Post
from felix_website.apps.tags.models import Tag

info_dict = {
    'queryset': Post.objects.all().select_related(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('django.views.generic.date_based',
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', 'object_detail', dict(info_dict, slug_field='slug')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
    (r'^$', 'archive_index', dict(info_dict, allow_empty=True)),
)

urlpatterns += patterns('apps.blog.views',
    (r'^post/create/$', 'add_edit_post'),
    (r'^post/(?P<id>\d+)/update/$', 'add_edit_post'),
    (r'^post/(?P<id>\d+)/mail/$', 'mail_post'),
    (r'^post/(?P<id>\d+)/delete/$', 'delete_post'),
)
