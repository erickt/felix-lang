from django.http import HttpResponse

from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

def style(request):
    try:
        style = get_style_by_name(request.GET['style'])
    except (KeyError, ValueError):
        style = 'autumn'

    formatter = HtmlFormatter(style=style)
    return HttpResponse(formatter.get_style_defs('.highlight'), mimetype='text/css')
