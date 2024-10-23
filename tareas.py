
from fastapi import HTTPException
from typing import Optional, Any, Dict
from datetime import datetime
from errors import TaskNotFoundError, TaskInvalidFieldError
from models import Task
tasks = {
    0 : {
        'titulo': 'presentar el proyecto',
        'descripcion': 'Un padre nuestro y pa lante',
        'fecha_limite': '25/10/24',
        'prioridad': '5',
        'estado': 1
    },
    1 : {
        'titulo': 'str',
        'descripcion': 'str',
        'fecha_limite': 'DD/MM/YY',
        'prioridad': 2,
        'estado': 0
    }
}

def create(task:Task):
    new = task.dict(exclude_unset=True)
    # asigna el id mas baja disponible
    id = next(i for i in range(len(tasks) + 1) if i not in tasks)
    tasks[id] = new
    return new
def edit_task(task_id: int,task=tasks ,**kwargs: Dict[str, Any]) -> Optional[str]:
    # Verificar si la tarea existe
    if task_id not in tasks:
        mensaje = f"La tarea con ID {task_id} no se encontró."
        raise TaskNotFoundError(mensaje)
    

    new_date = {}
    # Iterar sobre los campos que se desean modificar
    for field, new_value in kwargs.items():
        # Verificar si el campo es válido
        if field in tasks[task_id]:
            # Actualizar el campo de la tarea
            tasks[task_id][field] = new_value
        else:
            raise TaskInvalidFieldError(field)
    
    return task[task_id]

def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    # Verificar si la tarea existe
    if task_id in tasks:
        return tasks[task_id]
    mensaje = f"La tarea con ID {task_id} no se encontró."
    raise TaskNotFoundError(mensaje)
def task_by_state(estado_buscado:int):
    tareas_filtradas = {}
    for id_tarea, info in tasks.items():
        print(id_tarea, info)
        print(estado_buscado)
        if info['estado'] == estado_buscado:
            tareas_filtradas[id_tarea] = info
            print(tareas_filtradas)
    return tareas_filtradas
def task_delete(id_task:int):
    dell_task = get_task_by_id(id_task)
    del tasks[id_task]
    return dell_task
if __name__ == '__main__':
    create(title='hola')
    create(description='tu')
    print(tasks)