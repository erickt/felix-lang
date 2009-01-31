import re

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.date_based import archive_index, archive_month, archive_day
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.forms as forms

from felix_website.apps.blog.models import Post


def authors_view(request, username, view, args, kwds):
    author = get_object_or_404(User, username=username)
    posts = author.post_set.all()
    info_dict = {
        'extra_context': {
            'author': author,
            'months': posts.dates('pub_date', 'month')[::-1],
            'authors': User.objects.all(),
        },
    }
    return view(request, *(args + (posts, 'pub_date')), **(dict(info_dict, **kwds)))

def authors_index(request, username):
    return authors_view(request, username, archive_index, (), {'allow_empty': True, 'template_name': 'authors/author_archive.html'})

def authors_month(request, username, year, month):
    return authors_view(request, username, archive_month, (year, month), {'template_name': 'authors/author_archive_month.html'})

def authors_day(request, username, year, month, day):
    return authors_view(request, username, archive_day, (year, month, day), {'template_name': 'authors/author_archive_day.html'})
