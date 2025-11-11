from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    username:str=Field(index=True)
    password_hash:str
    role:str=Field(default="admin")
    

    
    