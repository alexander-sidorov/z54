from django.urls import path

from task4.views import IndexView
from task4.views import ShowNumbersView
from task4.views import task

urlpatterns = [
    path("", task),
    path("check/", IndexView.as_view()),
    path("info/", ShowNumbersView.as_view()),
]
