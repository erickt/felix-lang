import re

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import django.newforms as forms

from apps.codeblocks.models import CodeBlock

# -----------------------------------------------------------------------------

class CodeBlockForm(forms.Form):
    title = forms.CharField(
            widget=forms.TextInput(attrs={'size': 50}))
    description = forms.CharField(
            help_text='optional. use html',
            required=False,
            widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}))
    filetype = forms.CharField(
            widget=forms.TextInput(attrs={'size': 50}))
    code = forms.CharField(
            widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}))
    output = forms.CharField(
            widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}))
    html = forms.CharField(
            help_text='optional. use html',
            required=False,
            widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}))


_re_slug = re.compile(r'\W+')

def add_edit_codeblock(request, slug=None):
    if request.method == 'POST':
        form = CodeBlockForm(request.POST)
        if form.is_valid():
            d = dict(
                title=form.clean_data['title'],
                slug=_re_slug.sub('-', form.clean_data['title'].lower()).strip('-'),
                description=form.clean_data['description'],
                filetype=form.clean_data['filetype'],
                code=form.clean_data['code'],
                output=form.clean_data['output'],
                html=form.clean_data['html'],
            )

            if slug is None:
                codeblock = CodeBlock(**d)
            else:
                codeblock = get_object_or_404(CodeBlock, pk=slug)
                codeblock.__dict__.update(d)

            codeblock.save()

            msg = 'The codeblock "%s" was added successfully.' % codeblock

            if request.has_key('_addanother'):
                request.user.message_set.create(
                        message=msg + ' ' + 'You may add another codeblock below.')

                return HttpResponseRedirect('/codeblocks/create/')
            elif request.has_key('_continue'):
                request.user.message_set.create(
                        message=msg + ' ' + 'You may edit it again below.')

                return HttpResponseRedirect('/codeblocks/%s/update' % codeblock.slug)
            else:
                request.user.message_set.create(message=msg)
                return HttpResponseRedirect('/codeblocks/')
    elif slug is None:
        form = CodeBlockForm()
    else:
        codeblock = get_object_or_404(CodeBlock, pk=slug)
        form = CodeBlockForm({
            'title': codeblock.title,
            'description': codeblock.description,
            'filetype': codeblock.filetype,
            'code': codeblock.code,
            'output': codeblock.output,
            'html': codeblock.html,
        })

    return render_to_response('default_create.html', {
        'form': form,
    }, RequestContext(request))
add_edit_codeblock = login_required(add_edit_codeblock)


def delete_codeblock(request, slug):
    codeblock = get_object_or_404(CodeBlock, pk=slug)

    if request.method == 'POST':
        if request.POST['post'] == 'yes':
            codeblock.delete()
            return HttpResponseRedirect('/codeblocks/')

    return render_to_response('default_delete.html', {
        'object': codeblock,
    }, RequestContext(request))
delete_codeblock = login_required(delete_codeblock)
