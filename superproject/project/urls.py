from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import include
from django.urls import path


def hello_world(request: HttpRequest):
    return HttpResponse("hello world")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hw/", hello_world),
    path("task4/", include("task4.urls")),
]
