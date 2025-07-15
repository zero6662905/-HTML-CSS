from fastapi import FastAPI, HTTPException
import uvicorn

from shemas.Task import Task

app = FastAPI(debug=True, docs_url="/")

tasks = []


@app.get("/tasks/")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}/")
def get_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post("/tasks/")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"status": "Task added"}


@app.put("/tasks/{task_id}/")
def update_task(task_id: int, updated_task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = updated_task.dict()
    return {"status": "Task updated"}


@app.delete("/tasks/{task_id}/")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"status": "Task deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)