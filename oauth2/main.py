from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import Annotated
from bd import Database
from schema.user import User, UserInDB
import crypt_functions
from datetime import datetime, timedelta
from jose import JWTError

app = FastAPI()
database = Database()

oauth2_schema = OAuth2PasswordBearer(tokenUrl = "/token")

CREDENTIAL_EXCEPTION = HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could not validate credentials",
                headers = {"WWW-Authenticate": "Bearer"}
)

INACTIVE_USER_EXCEPTION = HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Inactive user"
)

@app.get("/")
async def root():
    return RedirectResponse(
        url = "/docs"
    )

def get_user_current(token: Annotated[str, Depends(oauth2_schema)]):
    token_decode = crypt_functions.decode_token(token)
    if (token_decode is None):
        raise CREDENTIAL_EXCEPTION
    user = User(**get_user_db(token_decode).dict())
    return user

def get_user_current_disabled(user: Annotated[User, Depends(get_user_current)]):
    if (user.disabled):
        raise INACTIVE_USER_EXCEPTION
    return user

@app.get("/users/me")
async def get_users_me(user: Annotated[User, Depends(get_user_current_disabled)]):
    return user

def get_user_db(username: str):
    db_data = database.select(
        query = "SELECT * FROM oauth2.user WHERE username = %s",
        data = list({username})
    )
    if (db_data is not None):
        db_data = db_data[0]
        return UserInDB(**db_data)
    return []

def authenticate_user(username: str, password: str):
    userInDB = get_user_db(username)
    if (not userInDB):
        raise CREDENTIAL_EXCEPTION
    if (not crypt_functions.verify_password(password, userInDB.salt, userInDB.hashed_password)):
        raise CREDENTIAL_EXCEPTION
    return User(**userInDB.dict())
    

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes = 30)
    access_token_jwt = crypt_functions.create_token({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }


