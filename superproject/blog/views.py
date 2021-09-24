from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from blog.models import Post


class AllPostsView(ListView):
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(hidden=False)


class SinglePostView(DetailView):
    model = Post


class CreatePostView(CreateView):
    model = Post
    fields = "__all__"
