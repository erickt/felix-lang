import popen2
import cStringIO
import tempfile
import random
import smtplib
import time

from email.Utils import formatdate

from django.conf import settings
from django.core.mail import DNS_NAME, SafeMIMEText

# -----------------------------------------------------------------------------

def html2text(text):
    out = cStringIO.StringIO()
    f = tempfile.NamedTemporaryFile()
    try:
        print >> f, text
        f.flush()

        cmd = ['lynx', '-cfg', settings.LYNX_CFG, '-dump', '-force_html', f.name]
        
        outfile, infile = popen2.popen4(cmd)

        for line in outfile:
            if line.startswith('   '):
                out.write(line[3:])
            else:
                out.write(line)
    finally:
        f.close()

    return out.getvalue()

# -----------------------------------------------------------------------------

def create_message_id():
    try:
        random_bits = str(random.getrandbits(64))
    except AttributeError: # Python 2.3 doesn't have random.getrandbits().
        random_bits = ''.join([random.choice('1234567890') for i in range(19)])

    return "%d.%s@%s" % (time.time(), random_bits, DNS_NAME)


def send_mail(subject, body, from_email, recipient_list, message_id=None):
    msg = SafeMIMEText(body, settings.DEFAULT_CHARSET)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = recipient_list
    msg['Date'] = email.Utils.formatdate()
    msg['Message-ID'] = message_id or create_message_id()

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    try:
        server.sendmail(from_email, recipient_list, msg.as_string())
    finally:
        server.quit()
