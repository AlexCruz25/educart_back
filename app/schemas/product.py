

from typing import Optional
from sqlmodel import SQLModel


class ProductRead(SQLModel):
    name:str
    price:float
    category:str
    description:str
    image_url:str
    rating:float
    
class ProductCreate(SQLModel):
    name:str
    price:float
    category:str
    description:str
    image_url:str
    rating:float
    
class ProductUpdate(SQLModel):
    name:Optional[str]=None
    price:Optional[float]=None
    category:Optional[str]=None
    description:Optional[str]=None
    image_url:Optional[str]=None
    rating:Optional[float]=None