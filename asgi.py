from typing import Optional

from fastapi import Body
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.responses import Response

import db
import tg
from lessons import task_3
from users import gen_random_name
from users import get_user
from util import apply_cache_headers
from util import static_response

app = FastAPI()


@app.get("/tg/about")
def _():
    r = tg.getMe()
    return r


@app.get("/", response_class=HTMLResponse)
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("index.html")


@app.get("/img", response_class=Response)
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("image.jpg")


@app.get("/js", response_class=Response)
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("index.js")


@app.post("/task/3")
async def _(name: Optional[str] = Body(default=None)):
    result = task_3(name)
    return {"data": {"greeting": result}}


@app.post("/task/4")
async def _(request: Request, response: Response, data: str = Body(...)):
    user = get_user(request) or gen_random_name()
    response.set_cookie("user", user)

    if data == "stop":
        number = await db.get_number(user)
    else:
        number = await db.add_number(user, int(data))

    return {"data": {"n": number}}
