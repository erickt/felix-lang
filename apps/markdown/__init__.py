import os
import popen2
import tempfile

from django.conf import settings
from markdown import Markdown

# -----------------------------------------------------------------------------

md = Markdown(
    extensions=['pygments'],
    extension_configs={'pygments': [('formatter', 'tablehtml')]},
)

def markdown(text):
    print md
    return md.convert(text)
