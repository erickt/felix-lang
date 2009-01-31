import re

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.date_based import archive_index, archive_month, archive_day
from django.contrib.auth.decorators import login_required
from django import forms

from felix_website.apps.blog.models import Post
from felix_website.apps.tags.models import Tag


def tags_view(request, slug, view, args, kwds):
    tag = get_object_or_404(Tag, pk=slug)
    posts = tag.post_set.all()
    info_dict = {
        'extra_context': {
            'tag': tag,
            'months': posts.dates('pub_date', 'month')[::-1],
            'tags': Tag.objects.all(),
        },
    }
    return view(request, *(args + (posts, 'pub_date')), **(dict(info_dict, **kwds)))

def tags_index(request, slug):
    return tags_view(request, slug, archive_index, (), {'allow_empty': True, 'template_name': 'tags/tag_archive.html'})

def tags_month(request, slug, year, month):
    return tags_view(request, slug, archive_month, (year, month), {'template_name': 'tags/tag_archive_month.html'})

def tags_day(request, slug, year, month, day):
    return tags_view(request, slug, archive_day, (year, month, day), {'template_name': 'tags/tag_archive_day.html'})

# -----------------------------------------------------------------------------

class TagForm(forms.Form):
    title = forms.CharField(
            widget=forms.TextInput(attrs={'size': 50}))

_re_slug = re.compile(r'\W+')

def add_edit_tag(request, slug=None):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            d = dict(
                title=form.cleaned_data['title'],
                slug=_re_slug.sub('-', form.cleaned_data['title'].lower()).strip('-'),
            )

            if slug is None:
                tag = Tag(**d)
            else:
                tag = get_object_or_404(Tag, pk=slug)
                tag.__dict__.update(d)

            tag.save()

            msg = 'The tag "%s" was added successfully.' % tag

            if request.has_key('_addanother'):
                request.user.message_set.create(
                        message=msg + ' ' + 'You may add another tag below.')

                return HttpResponseRedirect('/tags/create/')
            elif request.has_key('_continue'):
                request.user.message_set.create(
                        message=msg + ' ' + 'You may edit it again below.')

                return HttpResponseRedirect('/tags/%s/update/' % tag.slug)
            else:
                request.user.message_set.create(message=msg)
                return HttpResponseRedirect('/tags/')
    elif slug is None:
        form = TagForm()
    else:
        tag = get_object_or_404(Tag, pk=slug)
        form = TagForm({
            'title': tag.title,
        })

    return render_to_response('default_create.html', {
        'form': form,
    }, RequestContext(request))
add_edit_tag = login_required(add_edit_tag)


def delete_tag(request, slug):
    tag = get_object_or_404(Tag, pk=slug)

    if request.method == 'POST':
        if request.POST['post'] == 'yes':
            tag.delete()
            return HttpResponseRedirect('/tags/')

    return render_to_response('default_delete.html', {
        'object': tag,
    }, RequestContext(request))
delete_tag = login_required(delete_tag)
