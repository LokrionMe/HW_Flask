from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Task(BaseModel):
    id: int
    title: str
    description: str
    is_delete: bool = False


task1 = Task(id=1, title='task1',
             description='task1 description')
Tasks: list[Task] = []
Tasks.append(task1)


@app.get("/tasks/", response_class=HTMLResponse)
async def tasks_list(request:Request):
    return templates.TemplateResponse("table.html", {"request":
request,"Tasks":Tasks})


@app.get("/tasks/{id}/")
async def task_id(id: int):
    for task in Tasks:
        if task.id == id:
            return task


@app.post("/tasks/")
async def task_add(id: int, title: str, desc: str):
    return Tasks.append(Task(id=id, title=title, description=desc))


@app.delete("/tasks/{id}/")
async def task_delete(id: int):
    for task in Tasks:
        if task.id == id:
            task.is_delete = True


@app.put("/task/{id}/")
async def root_add(id: int, desc: str):
    for task in Tasks:
        if task.id == id:
            task.description = desc
