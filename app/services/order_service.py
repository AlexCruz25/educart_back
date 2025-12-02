from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.cart import CartStatus
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderRead
from app.schemas.cart import CartSummary, CartItemRead
from app.models.user import User


class OrderService:
    TAX_RATE = 0.18

    def __init__(self, session: Session):
        self.session = session
        self.cart_repo = CartRepository(session)
        self.product_repo = ProductRepository(session)
        self.order_repo = OrderRepository(session)

    def create_from_cart(self, user: User) -> tuple[OrderRead, CartSummary]:
        cart = self.cart_repo.get_open_cart(user.id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay carrito para procesar.",
            )

        items = self.cart_repo.get_items(cart.id)
        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El carrito está vacío.",
            )

        product_map = {}
        for item in items:
            product = self.product_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto {item.product_id} no encontrado.",
                )
            if product.stock_actual < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Sin stock suficiente para {product.name}.",
                )
            product_map[item.product_id] = product

        # Calcular totales
        subtotal = 0.0
        order_items: list[OrderItem] = []
        summary_items: list[CartItemRead] = []

        for item in items:
            product = product_map[item.product_id]
            line_total = item.quantity * item.unit_price
            subtotal += line_total

            order_items.append(
                OrderItem(
                    order_id=0,
                    product_id=product.id,
                    name=product.name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=line_total,
                )
            )

            summary_items.append(
                CartItemRead(
                    product_id=product.id,
                    name=product.name,
                    category=product.category,
                    image_url=product.image_url,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=line_total,
                )
            )

        taxes = round(subtotal * self.TAX_RATE, 2)
        total = round(subtotal + taxes, 2)

        # ----------------------------
        #  ELIMINADO: with self.session.begin()
        #  USAMOS COMMIT MANUAL
        # ----------------------------

        # Crear orden
        order = Order(
            user_id=user.id,
            total=total,
            taxes=taxes,
            status=OrderStatus.CONFIRMED,
        )
        self.order_repo.create_order(order)

        # Agregar ítems de orden y actualizar stock
        for order_item in order_items:
            product = product_map[order_item.product_id]
            product.stock_actual -= order_item.quantity

            self.session.add(product)
            order_item.order_id = order.id
            self.order_repo.add_item(order_item)

        # Cerrar carrito
        cart.status = CartStatus.CHECKED_OUT
        self.session.add(cart)

        for cart_item in items:
            self.session.delete(cart_item)

        # Guardar cambios
        self.session.commit()

        # Refrescar orden
        refreshed_items = self.order_repo.get_items(order.id)
        self.session.refresh(order)

        order_read = OrderRead(
            id=order.id,
            status=order.status,
            total=order.total,
            taxes=order.taxes,
            items=[
                {
                    "product_id": i.product_id,
                    "name": i.name,
                    "quantity": i.quantity,
                    "unit_price": i.unit_price,
                    "line_total": i.line_total,
                }
                for i in refreshed_items
            ],
        )

        summary = CartSummary(items=summary_items, subtotal=subtotal, taxes=taxes, total=total)

        return order_read, summary
