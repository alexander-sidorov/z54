from fastapi import FastAPI
from fastapi import Query

from lessons import task_3_1

app = FastAPI()


@app.get("/")
def handler():
    return "hello world"


@app.get("/task/3/1/")
def handler(name: str = Query(...)):
    result = task_3_1(name)
    return {"result": result}
