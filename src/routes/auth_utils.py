from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.config.database import get_db
from fastapi import  Depends, HTTPException, status
from provider import token_provider
from jose import JWTError
from dependencies.users import UserDependencies

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def get_user_logged_in(token: str = Depends(oauth2_schema), session: Session=Depends(get_db)):
    try:
        user = token_provider.verify_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    
    take_user = UserDependencies(session).read_email(user)

    if not take_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    
    return take_user