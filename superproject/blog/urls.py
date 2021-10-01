from django.urls import include
from django.urls import path
from rest_framework import routers

from blog import views

app_name = "blog"

router = routers.DefaultRouter()
router.register("posts", views.PostViewSet)

urlpatterns = [
    path("", views.AllPostsView.as_view(), name="all"),
    path("<int:pk>/", views.SinglePostView.as_view(), name="single"),
    path("<int:pk>/delete/", views.DeletePostView.as_view(), name="delete"),
    path("<int:pk>/update/", views.UpdatePostView.as_view(), name="update"),
    path("api/", include(router.urls)),
    path("new/", views.CreatePostView.as_view(), name="new"),
]
