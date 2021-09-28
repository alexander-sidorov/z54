from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from blog.models import Post


class MyView:
    fields = ["title", "content", "hidden"]
    model = Post
    success_url = reverse_lazy("blog:all")


class AllPostsView(MyView, ListView):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class SinglePostView(MyView, DetailView):
    pass


class CreatePostView(MyView, CreateView):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class UpdatePostView(MyView, UpdateView):
    pass


class DeletePostView(MyView, DeleteView):
    pass
