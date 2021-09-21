from django.views.generic import ListView

from blog.models import Post


class AllPostsView(ListView):
    model = Post
