from typing import List

from sqlmodel import SQLModel

from app.schemas.cart import CartSummary
from app.models.order import OrderStatus


class OrderItemRead(SQLModel):
    product_id: int
    name: str
    quantity: int
    unit_price: float
    line_total: float

    class Config:
        orm_mode = True


class OrderRead(SQLModel):
    id: int
    status: OrderStatus
    total: float
    taxes: float
    items: List[OrderItemRead]

    class Config:
        orm_mode = True


class CheckoutResponse(SQLModel):
    detail: str
    order: OrderRead
    summary: CartSummary