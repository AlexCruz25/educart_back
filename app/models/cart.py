from enum import Enum
from typing import Optional

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from sqlmodel import Field, SQLModel

class CartStatus(str, Enum):
    OPEN = "open"
    CHECKED_OUT = "checked_out"


class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: CartStatus = Field(default=CartStatus.OPEN)


class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(
        sa_column=Column(Integer, ForeignKey("cart.id", ondelete="CASCADE")),
    )
    product_id: int = Field(
        sa_column=Column(Integer, ForeignKey("product.id", ondelete="CASCADE")),
    )
    quantity: int = Field(default=1)
    unit_price: float