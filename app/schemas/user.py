
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str
    password: str
    role: str = "user"
    
    
    

class UserRead(SQLModel):
    id: int
    username: str
    role: str
    
class UserLogin(SQLModel):
    username:str
    password:str
    