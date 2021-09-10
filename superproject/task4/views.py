from django.http import HttpRequest
from django.http import HttpResponse

# from task4.models import Numbers


def view(request: HttpRequest) -> HttpResponse:
    # name = ''
    # try:
    #     obj = Numbers.objects.get(name=name)
    #     n = obj.n
    # except Numbers.DoesNotExist:
    #     n = -1

    # return HttpResponse(str(n))
    return HttpResponse("hello from task4")
