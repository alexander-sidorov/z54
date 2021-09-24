from django.urls import path

from blog import views

urlpatterns = [
    path("", views.AllPostsView.as_view()),
    path("<int:pk>/", views.SinglePostView.as_view()),
    path("<int:pk>/delete/", views.DeletePostView.as_view()),
    path("<int:pk>/update/", views.UpdatePostView.as_view()),
    path("new/", views.CreatePostView.as_view()),
]
