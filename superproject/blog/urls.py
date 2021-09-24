from django.urls import path

from blog import views

urlpatterns = [
    path("", views.AllPostsView.as_view()),
    path("<int:pk>/", views.SinglePostView.as_view()),
    path("new/", views.CreatePostView.as_view()),
]
