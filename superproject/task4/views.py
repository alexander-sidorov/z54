import json
import traceback
from random import choice
from string import ascii_lowercase
from typing import Optional
from typing import Tuple
from typing import Union

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ipware import get_client_ip

from task4.models import Check
from task4.models import CheckT
from task4.models import Numbers


def get_user_name(request: HttpRequest) -> Optional[str]:
    name = request.headers.get("x-user") or None
    return name


def create_new_user_name() -> str:
    def word() -> str:
        return "".join(choice(ascii_lowercase) for _ in range(6))

    return "-".join(word() for _ in "123")


def set_user_name(response: HttpResponse, name: str) -> None:
    response.headers["x-user"] = name


def add_number(name: str, number: int):
    obj: Tuple[Numbers, bool] = Numbers.objects.get_or_create(name=name)
    rec, _created = obj
    rec.n += number
    rec.save()
    return rec.n


def validate_number(number: int) -> None:
    lower_bound, upper_bound = -100, 100
    if not (lower_bound <= number <= upper_bound):
        raise ValueError(
            f"number {number} is not in range {(lower_bound, upper_bound)}"
        )


def parse_payload(request: HttpRequest) -> Union[str, int, None]:
    if not request.body:
        raise ValueError("non-empty body is required")

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError as err:
        raise ValueError(f"malformed payload: {request.body!r} ({err})") from err

    if isinstance(payload, int):
        validate_number(payload)
    elif payload != "stop":
        raise ValueError(
            f"value {payload!r} is not acceptable: MUST be either int, or 'stop'"
        )

    return payload


class UnprocessableEntityResponse(JsonResponse):
    status_code = 422


@csrf_exempt
@require_http_methods(["POST"])
def task(request: HttpRequest) -> HttpResponse:
    name = get_user_name(request)
    if not name:
        raise PermissionDenied(json.dumps("header X-USER is not set"))

    try:
        payload = parse_payload(request)
    except ValueError as err:
        response = UnprocessableEntityResponse(str(err), safe=False)
    else:
        if isinstance(payload, int):
            current = add_number(name, payload)
        elif payload == "stop":
            current = add_number(name, 0)
        else:
            current = None

        response = JsonResponse(
            current,
            safe=False,
        )

    set_user_name(response, name)
    return response


@csrf_exempt
def check(request: HttpRequest) -> HttpResponse:
    resp_payload = {"ok": False}

    try:
        ip, _routable = get_client_ip(request)

        obj: CheckT = CheckT.parse_raw(request.body)
        obj.ip = ip

        dbobj = Check(**obj.dict())
        dbobj.save()

        obj = CheckT.from_orm(dbobj)
        resp_payload.update(
            {
                "ok": True,
                "data": obj.dict(),
            }
        )

    except Exception as err:
        resp_payload["description"] = str(err)
        resp_payload["tb"] = traceback.format_exc()

    return JsonResponse(resp_payload, status=200 if resp_payload["ok"] else 500)


@csrf_exempt
def index(request: HttpRequest) -> HttpResponse:
    if request.method.upper() == "GET":
        return render(request, "task4/index.html")
    return check(request)
