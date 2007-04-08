from django import template
from apps.codeblocks.models import CodeBlock
import datetime
import random

class RandomCodeBlockNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        d = CodeBlock.objects.all()
        if not d:
            return ''

        i = random.randint(0, d.count() - 1)
        context[self.varname] = d[i]
        return ''

def do_get_random_codeblock(parser, token):
    """
    {% get_random_codeblock as codeblock %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return RandomCodeBlockNode(bits[2])


register = template.Library()
register.tag('get_random_codeblock', do_get_random_codeblock)
