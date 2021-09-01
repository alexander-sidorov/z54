from typing import Optional

import httpx
from fastapi import Body
from fastapi import FastAPI
from fastapi import Header
from fastapi.requests import Request
from fastapi.responses import Response

import db
import tg
from lessons import task_3
from users import gen_random_name
from users import get_user
from util import apply_cache_headers
from util import authorize
from util import static_response

app = FastAPI()


@app.get("/tg/about")
async def _(client: httpx.AsyncClient = tg.Telegram):
    user = await tg.getMe(client)
    return user


@app.get("/tg/webhook")
async def _(client: httpx.AsyncClient = tg.Telegram):
    whi = await tg.getWebhookInfo(client)
    return whi


@app.post("/tg/webhook")
async def _(
    client: httpx.AsyncClient = tg.Telegram,
    whi: tg.WebhookInfo = Body(...),
    authorization: str = Header(""),
):
    authorize(authorization)
    webhook_set = await tg.setWebhook(client, whi)
    whi = await tg.getWebhookInfo(client)
    return {
        "ok": webhook_set,
        "webhook": whi,
    }


@app.get("/")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("index.html")


@app.get("/img")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("image.jpg")


@app.get("/js")
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
