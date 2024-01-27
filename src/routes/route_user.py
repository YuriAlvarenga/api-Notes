from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas.schemas import UserBase, Note
from db.config.database import get_db
from dependencies.users import UserDependencies
from typing import List


router = APIRouter()


######### Rotas de users #############

@router.get('/users', response_model=List[Note])
def read_users(session: Session = Depends(get_db)):
    users = UserDependencies(session).read_user()
    return users

@router.get('/users/{id}', response_model=Note)
def get_users_by_id(id:int, session:Session = Depends(get_db)):
    user_by_id = UserDependencies(session).get_user_by_id(id)
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário {id} não Localizado')
    return user_by_id


@router.put('/users', response_model=UserBase)
def update_users(user: UserBase, session: Session = Depends(get_db)):
    UserDependencies(session).update_user(user)
    return user

@router.delete('/users/{user_id}')
def remove_users(user_id: int, session: Session = Depends(get_db)):
    UserDependencies(session).delete_user(user_id)
    return {'mensage': 'Removido com sucesso'}

