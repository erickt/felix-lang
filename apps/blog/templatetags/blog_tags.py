import datetime

from django import template
from django.contrib.auth.models import User

from apps.blog.models import Post
from apps.tags.models import Tag

register = template.Library()

# -----------------------------------------------------------------------------

class LatestBlogPostsNode(template.Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        context[self.varname] = list(Post.objects.filter(pub_date__lte=datetime.datetime.now())[:self.num])
        return ''

def do_get_latest_blog_posts(parser, token):
    """
    {% get_latest_blog_posts 2 as latest_posts %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
    return LatestBlogPostsNode(bits[1], bits[3])

register.tag('get_latest_blog_posts', do_get_latest_blog_posts)

# -----------------------------------------------------------------------------

class QueryNode(template.Node):
    def __init__(self, query, varname):
        self.query = query
        self.varname = varname

    def render(self, context):
        context[self.varname] = list(self.query)
        return ''

def do_get_post_dates(parser, token):
    """
    {% get_post_dates month as months %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
    return QueryNode(Post.objects.dates('pub_date', bits[1])[::-1], bits[3])

def do_get_post_tags(parser, token):
    """
    {% get_post_tags as tags %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return QueryNode(Tag.objects.all(), bits[2])

def do_get_post_authors(parser, token):
    """
    {% get_post_authors as authors %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return QueryNode(User.objects.all(), bits[2])


register.tag('get_post_dates', do_get_post_dates)
register.tag('get_post_tags', do_get_post_tags)
register.tag('get_post_authors', do_get_post_authors)
