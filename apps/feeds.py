from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from apps.blog.models import Post

class LatestEntries(Feed):
    title = 'felix-lang.org news'
    link = '/feeds/'
    description = 'Updates on blog posts.'

    def items(self):
        return Post.objects.order_by('-pub_date')[:5]

    def item_author_name(self, item):
        return item.author.first_name + ' ' + item.author.last_name
