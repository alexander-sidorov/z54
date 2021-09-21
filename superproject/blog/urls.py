from django.urls import path

from blog.views import AllPostsView
from blog.views import SinglePostView

urlpatterns = [
    path("", AllPostsView.as_view()),
    path("<int:pk>/", SinglePostView.as_view()),
]
