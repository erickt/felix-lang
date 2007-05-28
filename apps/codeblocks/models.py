from django.db import models

class CodeBlock(models.Model):
    title = models.CharField(maxlength=200)
    slug = models.SlugField(primary_key=True)
    description = models.TextField(blank=True)
    filetype = models.CharField(maxlength=30, blank=True)
    code = models.TextField()
    output = models.TextField()
    html_code = models.TextField(blank=True, help_text='leave blank to autogenerate')
    html_output = models.TextField(blank=True)

    class Admin:
        fields = (
                (None, {'fields': ('title', 'slug', 'description', 'filetype', 'code', 'html', 'output')}),
                )

    class Meta:
        ordering = ('slug',)
        get_latest_by = 'slug'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/codeblocks/' + self.slug
