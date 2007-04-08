import os
import popen2
import tempfile

from django.conf import settings

# -----------------------------------------------------------------------------

def markdown(text):
    f = tempfile.NamedTemporaryFile()
    try:
        print >> f, text
        f.flush()

        cmd = [os.path.join(settings.BIN_DIR, 'MultiMarkdown.pl'), f.name]
        
        outfile, infile = popen2.popen4(cmd)

        return '%s' % outfile.read().strip()
    finally:
        f.close()

