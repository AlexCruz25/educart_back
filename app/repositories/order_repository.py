from typing import List

from sqlmodel import Session, select

from app.models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_order(self, order: Order) -> Order:
        self.session.add(order)
        self.session.flush()
        return order

    def add_item(self, item: OrderItem) -> OrderItem:
        self.session.add(item)
        self.session.flush()
        return item

    def get_items(self, order_id: int) -> List[OrderItem]:
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        return self.session.exec(statement).all()