from typing import List, Optional
from sqlmodel import Session, select, delete

from sqlalchemy import asc, desc, or_
from app.models.product import Product
from app.models.cart import CartItem

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_all(self) -> List[Product]:
        return self.session.exec(select(Product)).all()

    def get_filtered(
        self,
        *,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        search: str | None = None,
        sort_by: str | None = None,
    ) -> List[Product]:
        statement = select(Product)
        if category:
            statement = statement.where(Product.category.ilike(f"%{category}%"))
        if min_price is not None:
            statement = statement.where(Product.price >= min_price)
        if max_price is not None:
            statement = statement.where(Product.price <= max_price)
        if min_rating is not None:
            statement = statement.where(Product.rating >= min_rating)

        if search:
            term = f"%{search}%"
            statement = statement.where(
                or_(Product.name.ilike(term), Product.description.ilike(term))
            )
        if sort_by == "price_asc":
            statement = statement.order_by(asc(Product.price))
        elif sort_by == "price_desc":
            statement = statement.order_by(desc(Product.price))
        elif sort_by == "name_asc":
            statement = statement.order_by(asc(Product.name))
        elif sort_by == "name_desc":
            statement = statement.order_by(desc(Product.name))
        elif sort_by == "rating_desc":
            statement = statement.order_by(desc(Product.rating))
        return self.session.exec(statement).all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.get(Product, product_id)
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        statement = select(Product).where(Product.sku == sku)
        return self.session.exec(statement).first()

    def update(self, product_id: int, product_data: Product | dict) -> Optional[Product]:
        db_product = self.session.get(Product, product_id)
        if not db_product:
            return None

        if hasattr(product_data, "dict"):
            update_data = product_data.dict(exclude_unset=True)
        else:
            update_data = product_data

        for key, value in update_data.items():
            setattr(db_product, key, value)

        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product

    def delete(self, product_id: int) -> bool:
        db_product = self.session.get(Product, product_id)
        if not db_product:
            return False

        statement = delete(CartItem).where(CartItem.product_id == product_id)
        self.session.exec(statement)
        self.session.commit()

        self.session.delete(db_product)
        self.session.commit()

        return True
