from django.urls import path

from task4.views import check
from task4.views import index

urlpatterns = [
    path("", index),
    path("check/", check),
]
