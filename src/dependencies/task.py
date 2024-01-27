from sqlalchemy.orm import Session, joinedload
from db.schemas import schemas
from db.models import models
from sqlalchemy import select, update, delete

class TaskDependecies():
    

    def __init__(self, session: Session):
        self.session = session

    def read_task(self):
        tasks = self.session.query(models.Task).all()
        return tasks

    def create_task(self, tarefaDependencies: schemas.TaskBase, user_id: int):
        db_task = models.Task(
            title = tarefaDependencies.title,
            task = tarefaDependencies.task,
            dateCreate = tarefaDependencies.dateCreate,
            priority = tarefaDependencies.priority,
            user_id = user_id
            )
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task
    
    
    def update_task(self, id: int, task: schemas.TaskBase):
        statement_update = update(models.Task).where(models.Task.id == id).values(
                                                                                        title = task.title,
                                                                                        task = task.task,
                                                                                        priority = task.priority
                                                                                    )
        self.session.execute(statement_update)
        self.session.commit()
    
    def delete_task(self, task_id: int):
        statement = delete(models.Task).where(models.Task.id == task_id)

        self.session.execute(statement)
        self.session.commit()

    def get_by_id(self, id: int):
        search_task = select(models.Task).where(models.Task.id == id)
        task_by_id = self.session.execute(search_task).scalars().first()
        return task_by_id
    
    def get_task_by_user(self, user_id: int):
        query = select(models.Task).where(models.Task.user_id == user_id)
        resultado = self.session.execute(query).scalars().all()
        return resultado