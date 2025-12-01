from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, SQLModel


class OrderStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    total: float
    taxes: float
    status: OrderStatus = Field(default=OrderStatus.CONFIRMED)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(sa_column=Column(Integer, ForeignKey("order.id", ondelete="CASCADE")))
    product_id: int
    name: str
    quantity: int
    unit_price: float
    line_total: float