from django import template
from apps.blog.models import Post
from apps.vimcolor import highlight
import datetime

class SyntaxHighlightNode(template.Node):
    def __init__(self, nodelist, filetype=None):
        self.nodelist = nodelist
        self.filetype = filetype

    def render(self, context):
        output = self.nodelist.render(context)

        return highlight(output, self.filetype)

       
def do_syntax_highlight(parser, token):
    nodelist = parser.parse(('endhighlight',))
    parser.delete_first_token()
    
    bits = token.contents.split()
    if len(bits) > 2:
        raise template.TemplateSyntaxError, "'%s' tag takes one or two arguments" % bits[0]
    if len(bits) == 1:
        return SyntaxHighlightNode(nodelist)
    else:
        return SyntaxHighlightNode(nodelist, bits[1])

register = template.Library()
register.tag('highlight', do_syntax_highlight)
