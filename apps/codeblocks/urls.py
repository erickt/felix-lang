from django.conf.urls.defaults import *
from models import CodeBlock

info_dict = {
    'queryset': CodeBlock.objects.order_by('slug'),

}

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', dict(info_dict, allow_empty=True)),
)

urlpatterns += patterns('apps.codeblocks.views',
    (r'^create/$', 'add_edit_codeblock'),
    (r'^update/(?P<slug>[\w-]+)/$', 'add_edit_codeblock'),
    (r'^delete/(?P<slug>[\w-]+)/$', 'delete_codeblock'),
)
