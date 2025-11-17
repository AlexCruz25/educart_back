from sqlmodel import Field, SQLModel

from app.models.user import UserRole



class UserCreate(SQLModel):
    username: str
    password: str
    role: UserRole | None = Field(default=UserRole.USER)
    
    
    

class UserRead(SQLModel):
    id: int
    username: str
    role: UserRole
    
class UserLogin(SQLModel):
    username: str
    password: str
    