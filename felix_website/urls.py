import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *

from felix_website.apps.feeds import LatestEntries

admin.autodiscover()

feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    (r'^codeblocks/', include('felix_website.apps.codeblocks.urls')),
    (r'^blog/', include('felix_website.apps.blog.urls')),
    (r'^tags/', include('felix_website.apps.tags.urls')),
    (r'^authors/', include('felix_website.apps.authors.urls')),
    (r'^pygments/', include('felix_website.apps.pygments.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

if os.path.exists(os.path.join(settings.PROJECT_DIR, 'urls_local.py')):
    execfile(os.path.join(settings.PROJECT_DIR, 'urls_local.py'))
