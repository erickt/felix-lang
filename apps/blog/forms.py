from django import forms

from felix_website.apps.tags.models import Tag
from felix_website.apps.blog.models import Post, BODY_TYPE_CHOICES

# -----------------------------------------------------------------------------

class PostForm(forms.Form):
    title = forms.CharField(
            widget=forms.TextInput(attrs={'size': 50}))
    tags = forms.models.ModelMultipleChoiceField(
            Tag.objects.all(),
            required=False)
    format = forms.ChoiceField(
            choices=BODY_TYPE_CHOICES)
    body = forms.CharField(
            widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}))


class MailForm(forms.Form):
    to = forms.CharField(
            widget=forms.TextInput(attrs={'size': 50}))
    title = forms.CharField(
            widget=forms.TextInput(attrs={'size': 50}))
    body = forms.CharField(
            widget=forms.Textarea(attrs={'rows': '10', 'cols': '40'}))

