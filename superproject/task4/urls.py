from django.urls import path

from task4.views import index
from task4.views import task

urlpatterns = [
    path("", task),
    path("check/", index),
]
