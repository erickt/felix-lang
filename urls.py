import os
from django.conf import settings
from django.contrib.comments.models import FreeComment
from django.conf.urls.defaults import *

comments_info_dict = {
    'queryset': FreeComment.objects.all(),
    'paginate_by': 15,
}

urlpatterns = patterns('',
    (r'^codeblocks/', include('felix_website.apps.codeblocks.urls')),
    (r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict),
    (r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^blog/', include('felix_website.apps.blog.urls')),
    (r'^tags/', include('felix_website.apps.tags.urls')),
    (r'^authors/', include('felix_website.apps.authors.urls')),
    (r'^profiles/', include('felix_website.apps.profiles.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
)

if os.path.exists(os.path.join(settings.PROJECT_DIR, 'urls_local.py')):
    execfile(os.path.join(settings.PROJECT_DIR, 'urls_local.py'))

urlpatterns += patterns('',
     (r'', include('django.contrib.flatpages.urls')),
)
