import re
import md5
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import django.newforms as forms
from django.conf import settings

from apps.blog.models import Post, BODY_TYPE_CHOICES
from apps.tags.models import Tag
from apps.blog.forms import PostForm, MailForm

from apps.markdown import markdown
from apps.mail import send_mail, create_message_id, html2text

# -----------------------------------------------------------------------------

_re_slug = re.compile(r'\W+')

def add_edit_post(request, id=None):
    post = None
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            html_body = form.cleaned_data['body']
            if form.cleaned_data['format'] == 'markdown':
                html_body = markdown(html_body)
                
            d = dict(
                author=request.user, 
                title=form.cleaned_data['title'],
                slug=_re_slug.sub('-', form.cleaned_data['title'].lower()).strip('-'),
                format=form.cleaned_data['format'],
                body=form.cleaned_data['body'],
                html_body=html_body,
            )

            if id is None:
                post = Post(pub_date=datetime.now(), **d)
            else:
                post = get_object_or_404(Post, pk=id)
                post.__dict__.update(d)
                post.tags = form.cleaned_data['tags']

            # check to make sure we don't have a blog with the same title
            posts = Post.objects
            if id is not None:
                posts = posts.exclude(id=post.id)

            if posts.filter(
                    pub_date__year=post.pub_date.year, 
                    pub_date__month=post.pub_date.month, 
                    pub_date__day=post.pub_date.day, 
                    title=post.title).count():
                form.errors.setdefault('title', []).append('must enter in a unique title for the day.')
            elif request.has_key('_preview'):
                pass
            else:
                post.save()

                if id is None:
                    post.tags = form.cleaned_data['tags']
                    post.save()

                msg = 'The post "%s" was added successfully.' % post

                if request.has_key('_addanother'):
                    request.user.message_set.create(
                            message=msg + ' ' + 'You may add another post below.')

                    return HttpResponseRedirect('/blog/post/create/')
                elif request.has_key('_continue'):
                    request.user.message_set.create(
                            message=msg + ' ' + 'You may edit it again below.')

                    return HttpResponseRedirect('/blog/post/%s/update' % post.id)
                elif request.has_key('_sendmail'):
                    return HttpResponseRedirect('/blog/post/%s/mail' % post.id)
                else:
                    request.user.message_set.create(message=msg)
                    return HttpResponseRedirect('/blog/')
    elif id is None:
        form = PostForm()
    else:
        post = get_object_or_404(Post, pk=id)
        form = PostForm({
            'title': post.title,
            'slug': post.slug,
            'tags': post.tags.all(),
            'format': post.format,
            'body': post.body,
        })

    return render_to_response('blog/post_create.html', {
        'form': form,
        'object': post,
    }, RequestContext(request))
add_edit_post = login_required(add_edit_post)

# -----------------------------------------------------------------------------

def mail_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            post.message_id = create_message_id()

            send_mail(
                form.cleaned_data['title'],
                form.cleaned_data['body'],
                '%s %s <%s>' % (request.user.first_name, request.user.last_name, request.user.email),
                [form.cleaned_data['to']],
                post.message_id,
            )
            post.save()

            request.user.message_set.create(
                    message='The post "%s" was mailed successfully.' % \
                    form.cleaned_data['title'])
            return HttpResponseRedirect('/blog/')
    else:
        if post.format == 'markdown':
            body = post.body
        else:
            body = html2text(post.body)

        form = MailForm({
            'to': 'felix-language@googlegroups.com',
            'title': post.title,
            'body': body,
        })

    return render_to_response('blog/post_mail.html', {
        'object': post,
        'form': form,
    }, RequestContext(request))
mail_post = login_required(mail_post)

# -----------------------------------------------------------------------------

def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'POST':
        if request.POST['post'] == 'yes':
            post.delete()
            return HttpResponseRedirect('/blog/')

    return render_to_response('default_delete.html', {
        'object': post,
    }, RequestContext(request))
delete_post = login_required(delete_post)
