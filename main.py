from fastapi import FastAPI, HTTPException
from errors import TaskInvalidFieldError, TaskNotFoundError
from tareas import tasks, get_task_by_id, create, task_by_state, task_delete, edit_task
from models import Task, IdDelete

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'bienvenido'}

@app.get('/task/all')
def all_task():
    return tasks

@app.get('/task/categoria/{state}')
def get_task_by_state(state:str):
    states = {
        'pendiente': 0,
        'proceso': 1,
        'finalizada': 2
    }
    if state not in states:
        mensaje = f"El estado {state} no es valido"
        raise TaskNotFoundError(mensaje)
    return task_by_state(states[state])

@app.put("/tasks/edit/{task_id}")
def edit_task_endpoint(task_id: int, task_edit: Task):
    # Convertir el modelo a diccionario excluyendo valores por defecto
    task_data = task_edit.dict(exclude_defaults=True)
    
    # Llamar a edit_task con el diccionario desempaquetado
    updated_task = edit_task(task_id, **task_data)
    return {"message": "Tarea actualizada con éxito", "task": updated_task}

@app.get('/task/{id_task}')
def get_task(id_task:int):
    task = get_task_by_id(id_task)
    return task

@app.post('/create')
def create_task(task:Task):
    new = create(task)
    return new
@app.delete('/delete')
def delete_task(id_task:IdDelete):
    return task_delete(id_task.id_task)
