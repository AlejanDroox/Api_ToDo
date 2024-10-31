from fastapi import FastAPI
from errors import TaskInvalidFieldError, TaskNotFoundError
from tareas import create, get_task_by_id, task_by_state, task_delete, edit_task, get_all_tasks
from models import Task, IdDelete


app = FastAPI()

@app.get('/')
def home():
    return {'message': 'bienvenido'}

@app.get('/task/all')
def all_task():
    return get_all_tasks()

@app.get('/task/categoria/{state}')
def get_task_by_state(state: str):
    states = {
        'pendiente': 0,
        'proceso': 1,
        'finalizada': 2
    }
    if state not in states:
        raise TaskNotFoundError(f"El estado {state} no es valido")
    return task_by_state(states[state])

@app.put("/tasks/edit/{task_id}")
def edit_task_endpoint(task_id: int, task_edit: Task):
    task_data = task_edit.dict(exclude_defaults=True)
    updated_task = edit_task(task_id, **task_data)
    return {"message": "Tarea actualizada con éxito", "task": updated_task}

@app.get('/task/{id_task}')
def get_task(id_task: int):
    return get_task_by_id(id_task)

@app.post('/create')
def create_task(task: Task):
    return create(task)

@app.delete('/delete')
def delete_task(id_task: IdDelete):
    return task_delete(id_task.id_task)