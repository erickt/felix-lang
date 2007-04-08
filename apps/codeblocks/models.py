from django.db import models
from apps.vimcolor import highlight

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
            self.html = highlight(
                    self.code.replace('\r\n', '\n'), 
                    self.filetype)

        return super(CodeBlock, self).save()

    def get_absolute_url(self):
        return '/codeblocks/' + self.slug
