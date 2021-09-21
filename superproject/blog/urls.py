from django.urls import path

from blog.views import AllPostsView

urlpatterns = [
    path("", AllPostsView.as_view()),
]
