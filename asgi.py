from fastapi import Body
from fastapi import FastAPI
from fastapi import Query
from starlette.requests import Request
from starlette.responses import Response

import db
from lessons import task_3_1
from users import gen_random_name
from users import get_user

app = FastAPI()


@app.get("/task/3/1")
async def handler(name: str = Query(...)):
    result = task_3_1(name)
    return {"result": result}


@app.post("/task/4")
async def handler(
    request: Request,
    response: Response,
    data: str = Body(...),
):
    user = get_user(request) or gen_random_name()
    response.set_cookie("user", user)

    if data == "stop":
        number = await db.get_number(user)
    else:
        number = await db.add_number(user, int(data))

    return {"data": {"n": number}}
