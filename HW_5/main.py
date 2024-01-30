from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional

app = FastAPI()

tasks = []

class Task(BaseModel):
    id: int
    header: str
    detail: str
    succesfull: Optional[int] = 0


# @app.post("/new_task/{header}")
# async def create_task(header: str, detail: str):
#     tasks.append(Task(header, detail))
#     return({"added task" : header})
@app.post("/new_task/")
async def create_task(task: Task):
    tasks.append(task)
    return ({"added task" : task})


@app.get("/")
async def read_tasks():
    return tasks


@app.get("/task/{id}")
async def get_task(id: int):
    for task in tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail='task not found')


@app.put("/task/{id}/")
async def update_task(id: int, task_new: Task):
    for task in tasks:
        if task.id == id:
            old_task = task.header
            task.id = task_new.id
            task.header = task_new.header
            task.detail = task_new.detail
            task.succesfull = task.succesfull
            return ({f"update task {old_task}" : task})
    raise HTTPException(status_code=404, detail='task not found')


@app.delete("/task/{id}/")
async def delete_task(id: int):
    for task in tasks:
        if task.id == id:
            task_rm = task
            tasks.remove(task)
            return ({"deleted task" : task_rm})
    raise HTTPException(status_code=404, detail='task not found')



if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )