from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from blog.models import Post

PAGE_SIZE = 50


class BlogMixin:
    fields = ["title", "content", "hidden"]
    model = Post
    success_url = reverse_lazy("blog:all")


class OwnerMixin:
    def get_queryset(self):
        x = super().get_queryset().filter(author=self.request.user)
        return x


class AllPostsView(BlogMixin, ListView):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False).order_by("pk")[:PAGE_SIZE]


class SinglePostView(BlogMixin, DetailView):
    pass


class CreatePostView(LoginRequiredMixin, BlogMixin, CreateView):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, BlogMixin, OwnerMixin, UpdateView):
    pass


class DeletePostView(LoginRequiredMixin, BlogMixin, OwnerMixin, DeleteView):
    pass
