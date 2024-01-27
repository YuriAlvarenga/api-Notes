from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), unique=True, index=True)

    task_from_user = relationship('Task', back_populates='usuario')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    task = Column(String, index=True)
    dateCreate = Column(String)
    priority = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), name='fk_user')
    usuario = relationship('User', back_populates='task_from_user')

