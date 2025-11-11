

from sqlmodel import Field, SQLModel


class Cart(SQLModel, table=True):
    id: int=Field(default=None, primary_key=True, index=True)
    
    user_id:int=Field(foreign_key="user.id")
    
    # carts: 