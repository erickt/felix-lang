from django.db import models
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

class CodeBlock(models.Model):
    title = models.CharField(maxlength=200)
    slug = models.SlugField(primary_key=True)
    description = models.TextField(blank=True)
    filetype = models.CharField(maxlength=30, blank=True)
    code = models.TextField()
    html = models.TextField(blank=True, help_text='leave blank to autogenerate')
    output = models.TextField()

    class Admin:
        fields = (
                (None, {'fields': ('title', 'slug', 'description', 'filetype', 'code', 'html', 'output')}),
                )

    class Meta:
        ordering = ('slug',)
        get_latest_by = 'slug'

    def __str__(self):
        return self.title

    def save(self):
        if not self.html:
            lexer = get_lexer_by_name(self.filetype, stripnl=True, encoding='UTF-8')
            self.html = highlight(self.code, lexer, HtmlFormatter())

        return super(CodeBlock, self).save()

    def get_absolute_url(self):
        return '/codeblocks/' + self.slug
