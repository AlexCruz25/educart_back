from typing import List, Optional

from sqlmodel import Session, select

from app.models.cart import Cart, CartItem, CartStatus


class CartRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_open_cart(self, user_id: int) -> Optional[Cart]:
        statement = select(Cart).where(
            Cart.user_id == user_id,
            Cart.status == CartStatus.OPEN,
        )
        return self.session.exec(statement).first()

    def create_cart(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart

    def get_or_create_cart(self, user_id: int) -> Cart:
        cart = self.get_open_cart(user_id)
        if cart is None:
            cart = self.create_cart(user_id)
        return cart

    def get_items(self, cart_id: int) -> List[CartItem]:
        statement = select(CartItem).where(CartItem.cart_id == cart_id)
        return self.session.exec(statement).all()

    def get_item_by_product(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        statement = select(CartItem).where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
        return self.session.exec(statement).first()

    def add_item(
        self,
        *,
        cart_id: int,
        product_id: int,
        quantity: int,
        unit_price: float,
    ) -> CartItem:
        item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def save_item(self, item: CartItem) -> CartItem:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_item(self, item: CartItem) -> None:
        self.session.delete(item)
        self.session.commit()

    def update_cart_status(self, cart: Cart, status: CartStatus) -> Cart:
        cart.status = status
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart

    def clear_cart(self, cart_id: int) -> None:
        items = self.get_items(cart_id)
        for item in items:
            self.session.delete(item)
        self.session.commit()