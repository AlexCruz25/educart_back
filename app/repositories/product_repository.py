from typing import List, Optional
from sqlmodel import Session, select, delete

from app.models.product import Product
from app.models.cart import CartItem
from app.repositories.cart_repository import CartRepository

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
        return self.session.exec(statement).all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.get(Product, product_id)

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

        # BORRAR LOS ITEMS DEL CARRITO ASOCIADOS
        statement = delete(CartItem).where(CartItem.product_id == product_id)
        self.session.exec(statement)
        self.session.commit()

        # AHORA SÍ BORRAR EL PRODUCTO
        self.session.delete(db_product)
        self.session.commit()

        return True
