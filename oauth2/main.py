from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import Annotated
from bd import Database

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl = "/token")

@app.get("/")
async def root():
    return RedirectResponse(
        url = "/docs"
    )

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(form_data.username, form_data.password)
    return { # Se debe devolver un diccionario con estos datos
        "access_token": "Tomatito",
        "token_type": "bearer"
    }

@app.get("/users/me")
async def get_users_me(token: Annotated[str, Depends(oauth2_schema)]):
    print("token: " + token)
    return "I am an user"
