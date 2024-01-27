from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas.schemas import TaskBase, SimpleTask, UserBase
from dependencies.task import TaskDependecies
from db.config.database import get_db
from typing import List
from routes.auth_utils import get_user_logged_in

router = APIRouter()


@router.get('/task')
def get_task_by_users(user: UserBase = Depends(get_user_logged_in), session: Session = Depends(get_db)):
    tasks = TaskDependecies(session).get_task_by_user(user.id)
    return tasks

@router.get('/task/{id}')
def get_tasks_by_id(id: int, session: Session = Depends(get_db)):
    task_by_id = TaskDependecies(session).get_by_id(id)
    if not task_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Nota {id} não localizada')
    return task_by_id

@router.post('/task', status_code = status.HTTP_201_CREATED, response_model = TaskBase)
def create_tasks(task: TaskBase, session: Session = Depends(get_db), current_user: UserBase = Depends(get_user_logged_in)):
    task_criada = TaskDependecies(session).create_task(task, user_id=current_user.id)
    return task_criada

@router.put('/task/{id}')
def update_tasks(id: int, task: TaskBase, session: Session = Depends(get_db)):
    TaskDependecies(session).update_task(id, task)
    task.id = id
    return task 

@router.delete('/task/{task_id}')
def remove_tasks(task_id: int, session: Session = Depends(get_db)):
    TaskDependecies(session).delete_task(task_id)
    return {'mensage': 'Removido com sucesso'}