import os
from django.conf import settings
from django.contrib import admin
from django.contrib.comments.models import Comment
from django.conf.urls.defaults import *

from felix_website.apps.feeds import LatestEntries

admin.autodiscover()

comments_info_dict = {
    'queryset': Comment.objects.all(),
    'paginate_by': 15,
}

feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    (r'^codeblocks/', include('felix_website.apps.codeblocks.urls')),
    (r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict),
    (r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^blog/', include('felix_website.apps.blog.urls')),
    (r'^tags/', include('felix_website.apps.tags.urls')),
    (r'^authors/', include('felix_website.apps.authors.urls')),
    (r'^pygments/', include('felix_website.apps.pygments.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

if os.path.exists(os.path.join(settings.PROJECT_DIR, 'urls_local.py')):
    execfile(os.path.join(settings.PROJECT_DIR, 'urls_local.py'))
