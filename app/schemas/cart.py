from typing import List, Optional

from sqlmodel import Field, SQLModel


class CartItemCreate(SQLModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItemUpdate(SQLModel):
    quantity: int = Field(gt=0)


class CartItemRead(SQLModel):
    product_id: int
    name: str
    category: Optional[str] = None
    image_url: Optional[str] = None
    quantity: int
    unit_price: float
    line_total: float


class CartSummary(SQLModel):
    items: List[CartItemRead] = Field(default_factory=list)
    subtotal: float = 0.0
    taxes: float = 0.0
    total: float = 0.0