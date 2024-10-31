import sqlite3
from contextlib import contextmanager
from typing import Dict, List, Optional
from models import Task
from errors import TaskNotFoundError, TaskInvalidFieldError

DATABASE_NAME = "todo.db"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_limite TEXT,
            prioridad INTEGER,
            estado INTEGER
        )
        ''')
        conn.commit()

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def execute_query(query: str, params: tuple = (), fetch_one: bool = False) -> Optional[Dict]:
    with get_db_connection() as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch_one:
            return cursor.fetchone()
        return cursor.fetchall()

def execute_action(query: str, params: tuple = ()) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def create(task: Task) -> Dict:
    query = '''
    INSERT INTO tasks (titulo, descripcion, fecha_limite, prioridad, estado)
    VALUES (?, ?, ?, ?, ?)
    '''
    task_dict = task.dict(exclude_unset=True)
    task_id = execute_action(query, tuple(task_dict.values()))
    return get_task_by_id(task_id)

def get_all_tasks() -> List[Dict]:
    return execute_query("SELECT * FROM tasks ORDER BY estado ASC, prioridad DESC")

def get_task_by_id(task_id: int) -> Optional[Dict]:
    task = execute_query("SELECT * FROM tasks WHERE id = ?", (task_id,), fetch_one=True)
    if not task:
        raise TaskNotFoundError(f"La tarea con ID {task_id} no se encontró.")
    return task

def edit_task(task_id: int, **kwargs) -> Dict:
    task = get_task_by_id(task_id)
    valid_fields = set(task.keys()) - {'id'}
    invalid_fields = set(kwargs.keys()) - valid_fields
    if invalid_fields:
        raise TaskInvalidFieldError(next(iter(invalid_fields)))

    update_fields = ', '.join([f"{key} = ?" for key in kwargs.keys()])
    query = f'UPDATE tasks SET {update_fields} WHERE id = ?'
    execute_action(query, tuple(kwargs.values()) + (task_id,))
    return get_task_by_id(task_id)

def task_by_state(estado_buscado: int) -> List[Dict]:
    return execute_query("SELECT * FROM tasks WHERE estado = ? ORDER BY prioridad DESC", (estado_buscado,))

def task_delete(id_task: int) -> Dict:
    task = get_task_by_id(id_task)
    execute_action("DELETE FROM tasks WHERE id = ?", (id_task,))
    return task


init_db()