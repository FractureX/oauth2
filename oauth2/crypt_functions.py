import hashlib
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "f264073512040916e631a3d913ef4465a5a054726dea80f55c9615681cc98d91"
ALGORITHM   = "HS256"
CREDENTIAL_EXCEPTION = HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could not validate credentials",
                headers = {"WWW-Authenticate": "Bearer"}
)

def encrypt_password(password: str, salt: str) -> str:
    return hashlib.sha1(string = (salt + password).encode("utf-8")).hexdigest()

def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    return (encrypt_password(password = password, salt = salt) == hashed_password)

def create_token(data: dict, time_expire: timedelta | None):
    data_copy = data.copy()
    if (time_expire is None):
        expires = datetime.utcnow() + timedelta(minutes = 15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(
        data_copy, 
        key = SECRET_KEY,
        algorithm = ALGORITHM
    )
    return token_jwt

def decode_token(token) -> str | None:
    try:
        token_decode = jwt.decode(token = token, key = SECRET_KEY, algorithms = [ALGORITHM])
        username = token_decode.get("sub")
        if (username == None):
            raise CREDENTIAL_EXCEPTION
        return username
    except JWTError as e:
        raise CREDENTIAL_EXCEPTION
    
