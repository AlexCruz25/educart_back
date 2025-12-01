from typing import Optional
from sqlmodel import SQLModel
from app.models.product import StockStatus

class ProductRead(SQLModel):
    id: int
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    rating: float = 0
    sku: str
    stock_actual: int
    stock_minimo: int
    stock_status: StockStatus

    class Config:
        orm_mode = True
    
class ProductCreate(SQLModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    rating: float = 0
    sku: str
    stock_actual: int = 0
    stock_minimo: int = 0
    
class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    sku: Optional[str] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None

    class Config:
        orm_mode = True