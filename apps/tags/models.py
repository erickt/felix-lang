from django.db import models

class Tag(models.Model):
    slug = models.SlugField(primary_key=True)
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title',)

    class Admin:
        fields = (
            (None, {'fields': ('title', 'slug')}),
            )

        list_display = ('slug', 'title')
        search_fields = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/tags/%s/' % self.slug
