import os

from django.core.asgi import get_asgi_application

from fastapi_app import app as application_fastapi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
fastapi_routes = {route.path for route in application_fastapi.routes}
application_django = get_asgi_application()


async def application(scope, send, receive):
    if scope["path"] in fastapi_routes:
        return await application_fastapi(scope, send, receive)
    else:
        return await application_django(scope, send, receive)
