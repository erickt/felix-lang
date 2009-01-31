from datetime import datetime
import md5

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings

from felix_website.apps.tags.models import Tag

BODY_TYPE_CHOICES = (
    ('markdown', 'markdown'),
    ('html', 'html'),
)

# -----------------------------------------------------------------------------

class Post(models.Model):
    pub_date = models.DateTimeField('publication date', blank=True)
    mod_date = models.DateTimeField('modification date', blank=True)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date')
    tags = models.ManyToManyField(Tag, blank=True)
    format = models.CharField(max_length=30, choices=BODY_TYPE_CHOICES)
    body = models.TextField(help_text='use html')
    html_body = models.TextField(blank=True)
    message_id = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/blog/%s/%s/' % (
                self.pub_date.strftime('%Y/%b/%d').lower(),
                self.slug,
                )

    def save(self):
        if not self.id:
            self.pub_date = datetime.now()

        if not self.message_id:
            self.message_id = ''

        self.mod_date = datetime.now()

        return super(Post, self).save()

    def has_tags(self):
        # protect against printing an object that's not in the db yet
        try:
            return self.tags.count()
        except ValueError:
            return False

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Tags', {'fields': ('tags',)}),
        ('Post', {'fields': ('author', 'title', 'format', 'body')}),
        ('Optional', {'fields': ('slug', 'pub_date', 'mod_date', 'html_body'), 'classes': 'collapse'}),
    )

    list_display = ('pub_date', 'mod_date', 'author', 'title', 'slug')
    search_fields = ('title', 'body')
    list_filter = ('pub_date',)
    date_hierarchy = 'pub_date'

admin.site.register(Post, PostAdmin)
