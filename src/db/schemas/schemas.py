from pydantic import BaseModel 
from typing import Optional, List
from datetime import date, datetime

class UserBase(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    password: str
    
    class Config:
        orm_mode = True

class LoginBase(BaseModel):
    email: str
    password: str


class TaskBase(BaseModel):
    id: Optional[int] = None
    title: str
    task: str
    dateCreate: date = datetime.now().date()
    priority: bool = False
    user_id: Optional[int] =None

    class Config:
        orm_mode = True



class SimpleTask(BaseModel):
    id: Optional[int] = None
    title: str
    task: str
    dateCreate: date = datetime.now().date()
    priority: bool = False

    class Config:
        orm_mode = True

class SimpleUser(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

    class Config:
        orm_mode = True


class Note(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    task_from_user: List[SimpleTask] =[]

    class Config:
        orm_mode = True

class NoteDetails(BaseModel):
    name: str
    dateCreate: date = datetime.now().date()

    class Config:
        orm_mode = True