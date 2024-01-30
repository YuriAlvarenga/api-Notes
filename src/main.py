from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import route_auth 
from routes import route_user
from routes import route_task




app = FastAPI()


# cors
origins = [
    'http://localhost:5173','*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



################### Rotas Auth ################
app.include_router(route_auth.router)

################### Rotas Usuários ################
app.include_router(route_user.router)

################### Rotas Tarefas ################
app.include_router(route_task.router)
