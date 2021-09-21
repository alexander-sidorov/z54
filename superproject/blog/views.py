from django.http import HttpRequest
from django.http import HttpResponse


def xxx(request: HttpRequest):
    return HttpResponse("blog works")
