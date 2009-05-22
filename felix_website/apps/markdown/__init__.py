import os
import popen2
import tempfile

from django.conf import settings
from markdown import Markdown

# -----------------------------------------------------------------------------

md = Markdown(
    extensions=['abbr', 'footnotes', 'tables', 'codehilite'],
    extension_configs={'codehilite': [('css_class', 'highlight')]},
)

def markdown(text):
    return md.convert(text)
