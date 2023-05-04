from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr | None = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str
    salt: str