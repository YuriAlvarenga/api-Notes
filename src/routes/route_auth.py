from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas.schemas import UserBase, SimpleUser, LoginBase, NoteDetails
from db.config.database import get_db
from dependencies.users import UserDependencies
from provider import hash_provider, token_provider
from routes.auth_utils import get_user_logged_in

router = APIRouter()

########## Create user and authentication #######

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=SimpleUser)
def create_users(user: UserBase, session: Session = Depends(get_db)):

    #### verifica a existencia do usuário ###
    find_user = UserDependencies(session).read_email(user.email)

    if find_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='E-mail já cadastrado')

    #### cria o usuário ###
    user.password = hash_provider.create_hash(user.password)
    user_created = UserDependencies(session).create_user(user)
    return user_created


#### Rota de login ####
@router.post('/login')
def login(login_data: LoginBase, session: Session = Depends(get_db)):
    email = login_data.email
    password = login_data.password

    user = UserDependencies(session).read_email(email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email incorreto')
    
    verify_password = hash_provider.verify_hash(password, user.password)
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Senha incorreta')


    #### Gerar Token JWT ####

    token = token_provider.create_access_token({'sub': user.email})
    return {'user': user.name, 'access_token': token }

#### rota do perfil ####
@router.get('/profile', response_model= NoteDetails)
def profile(user: UserBase = Depends(get_user_logged_in)):
    return user