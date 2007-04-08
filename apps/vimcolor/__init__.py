import os
import popen2
import tempfile
import re

def highlight(text, filetype=None):
    text = text.strip()
    f = tempfile.NamedTemporaryFile()
    try:
        print >> f, text
        f.flush()

        print [text]

        cmd = ['text-vimcolor', '--format', 'html']

        if filetype:
            cmd.append('--filetype')
            cmd.append(filetype)

        cmd.append(f.name)
        
        outfile, infile = popen2.popen4(cmd)

        return '%s' % outfile.read().strip()
    finally:
        f.close()


_code_re = re.compile(
    r'(.*?)'
    r'<code(?: type="([a-z]+)")?>(.*?)</code>'
    r'(.*)', 
    re.DOTALL)

def highlight_in_html(html):
    bodies = []

    def f(s):
        m = _code_re.match(s)
        if not m:
            bodies.append(s)
            return

        bodies.append(m.group(1))

        filetype = m.group(2)
        code = m.group(3)

        bodies.append('<code>')
        if filetype:
            bodies.append(highlight(code.replace('\r\n', '\n'), filetype))
        else:
            bodies.append(code)
        bodies.append('</code>')

        f(m.group(4))

    f(html)

    return ''.join(bodies) 
