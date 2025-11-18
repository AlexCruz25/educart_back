from typing import List, Optional
from pydantic import root_validator
from sqlmodel import Field, SQLModel


class CartItemCreate(SQLModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)

    @root_validator(pre=True)
    def support_camel_case(cls, values):  # type: ignore[override]
        product_id = values.get("product_id")
        product_id_camel = values.get("productId")
        if product_id is None and product_id_camel is not None:
            values["product_id"] = product_id_camel
        return values


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