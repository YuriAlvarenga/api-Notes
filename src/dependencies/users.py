from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update, delete
from db.schemas import schemas
from db.models import models


class UserDependencies():
    def __init__(self, session: Session):
        self.session = session

    def read_user(self):
        statemant = select(models.User)
        users = self.session.execute(statemant).scalars().all()
        return users
    
    def read_email(self, email):
        query = select(models.User).where(models.User.email == email)
        return self.session.execute(query).scalars().first()

    def create_user(self, user: schemas.UserBase):
        user_bd = models.User(
            name = user.name,
            email = user.email,
            password = user.password,
        )
        self.session.add(user_bd)
        self.session.commit()
        self.session.refresh(user_bd)
        return user_bd


    def update_user(self, user: schemas.UserBase):
        statement_update = update(models.User).where(models.User.id == user.id).values(
                                                                                    name = user.name,
                                                                                    email = user.email,
                                                                                    password = user.password,
                                                                                )
        self.session.execute(statement_update)
        self.session.commit()
    
    def delete_user(self, user_id: int):
        statement_user = delete(models.User).where(models.User.id == user_id)

        self.session.execute(statement_user)
        self.session.commit()

    def get_user_by_id(self, id: int):
        search_user = select(models.User).where(models.User.id == id)
        userId = self.session.execute(search_user).scalars().first()
        return userId