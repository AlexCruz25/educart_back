from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

class StockStatus(str, Enum):
    NORMAL = "normal"
    LOW = "low_stock"
    OUT = "out_of_stock"

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = 0
    sku: str = Field(index=True, sa_column_kwargs={"unique": True})
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)

    @property
    def stock_status(self) -> StockStatus:
        if self.stock_actual == 0:
            return StockStatus.OUT
        if self.stock_actual <= self.stock_minimo:
            return StockStatus.LOW
        return StockStatus.NORMAL
    
    