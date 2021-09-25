from django.urls import path

from blog import views

app_name = "blog"


urlpatterns = [
    path("", views.AllPostsView.as_view(), name="all"),
    path("<int:pk>/", views.SinglePostView.as_view(), name="single"),
    path("<int:pk>/delete/", views.DeletePostView.as_view(), name="delete"),
    path("<int:pk>/update/", views.UpdatePostView.as_view(), name="update"),
    path("new/", views.CreatePostView.as_view(), name="new"),
]
