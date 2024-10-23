from errors import ParameterNotValid
from pydantic import BaseModel,validator
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    """Modelo de datos para representar una tarea."""
    titulo: Optional[str] = 'Nueva Tarea'
    descripcion: Optional[str] = 'descripcion de Tarea'
    fecha_limite: Optional[str] = None
    prioridad: Optional[int] = 0
    estado: Optional[int] = 0

    @validator('fecha_limite', pre=True, always=True)
    def validate_dead_line(cls, v):
        if v is None:
            return None
        try:
            # Validar el formato de la fecha
            datetime.strptime(v, '%d/%m/%y')
            return v  # Devolver la cadena original
        except ValueError:
            raise ParameterNotValid(status_code=400, detail='La fecha debe estar en formato DD/MM/YY')
class TaskEdit(BaseModel):
    """Modelo de datos para editar una tarea.

    Atributos:
    - title (Optional[str]):.
    - descripcion (Optional[str]):.
    - dead_line (Optional[str]): La fecha límite para completar la tarea en formato DD/MM/YY.
    - priority (Optional[int]):"""
    title: Optional[str] = None
    descripcion: Optional[str] = None
    dead_line: Optional[str] = None
    priority: Optional[int] = None
    state: Optional[int] = None

    @validator('dead_line', pre=True, always=True)
    def validate_dead_line(cls, v):
        if v is None:
            return None
        try:
            # Validar el formato de la fecha
            datetime.strptime(v, '%d/%m/%y')
            return v  # Devolver la cadena original
        except ValueError:
            raise ParameterNotValid(status_code=400, detail='La fecha debe estar en formato DD/MM/YY')
class IdDelete(BaseModel):
    id_task: int