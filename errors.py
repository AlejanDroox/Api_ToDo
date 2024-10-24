from fastapi import HTTPException
class TaskError(HTTPException):
    """Clase base para errores relacionados con tareas."""
    pass

class TaskNotFoundError(TaskError):
    """Error cuando no se encuentra el parametro en el rango de datos."""
    def __init__(self, mensaje):

        super().__init__(status_code=404, detail=mensaje)

class TaskInvalidFieldError(TaskError):
    """Error cuando se intenta modificar un campo inválido de una tarea."""
    def __init__(self, field):
        mensaje = f"El campo '{field}' es inválido."
        super().__init__(status_code=400,detail=mensaje)
class ParameterNotValid(TaskError):
    """Error cuenado se envia un parametro de un tipo o formato invalido."""
    def __init__(self, param):
        mensaje = f"El parametro '{param}' es inválido. Verificar formato, sintaxis o tipo de dato."
        super().__init__(status_code=400,detail=mensaje)