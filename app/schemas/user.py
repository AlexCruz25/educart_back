from sqlmodel import SQLModel, Field
from app.models.user import UserRole


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    role: UserRole | None = Field(default=UserRole.USER)


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    role: UserRole
    
    class Config:
        orm_mode = True


class UserLogin(SQLModel):
    username: str
    password: str
