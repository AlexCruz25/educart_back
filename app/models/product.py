
from typing import Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    price:float
    category:str
    description:Optional[str]=None
    image_url:Optional[str]=None
    rating:Optional[float]=0
    
    