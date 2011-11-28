from haystack.indexes import *
from haystack import site
from blog.models import Post

class PostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='author')
    pub_date = DateTimeField(model_attr='date_published')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Post.objects.live()


site.register(Post, PostIndex)