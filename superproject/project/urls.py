from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("task4/", include("task4.urls")),
    path("login/", LoginView.as_view()),
]
