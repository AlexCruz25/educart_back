from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.cart import Cart, CartStatus
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartItemRead,
    CartSummary,
)
from app.models.user import User
from app.services.order_service import OrderService


class CartService:
    TAX_RATE = 0.18

    def __init__(self, session: Session):
        self.session = session
        self.repo = CartRepository(session)
        self.product_repo = ProductRepository(session)

    def _validate_stock(self, product_id: int, desired_qty: int) -> None:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado.",
            )
        if product.stock_actual <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Producto sin stock disponible.",
            )
        if desired_qty > product.stock_actual:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes agregar más unidades que las disponibles en inventario.",
            )


    def add_item(self, user: User, payload: CartItemCreate) -> CartSummary:
        if payload.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad debe ser mayor que cero.",
            )
        product = self.product_repo.get_by_id(payload.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado.",
            )
        cart = self.repo.get_or_create_cart(user.id)
        item = self.repo.get_item_by_product(cart.id, product.id)
        current_qty = item.quantity if item else 0
        desired_qty = current_qty + payload.quantity
        self._validate_stock(product.id, desired_qty)
        if item:
            item.quantity = desired_qty
            self.repo.save_item(item)
        else:
            self.repo.add_item(
                cart_id=cart.id,
                product_id=product.id,
                quantity=payload.quantity,
                unit_price=product.price,
            )
        return self._build_summary(cart)

    def update_item(self, user: User, product_id: int, payload: CartItemUpdate) -> CartSummary:
        if payload.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad debe ser mayor que cero.",
            )
        cart = self.repo.get_open_cart(user.id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay carrito activo.")
        item = self.repo.get_item_by_product(cart.id, product_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no está en el carrito.")
        self._validate_stock(product_id, payload.quantity)
        item.quantity = payload.quantity
        self.repo.save_item(item)
        return self._build_summary(cart)

    def remove_item(self, user: User, product_id: int) -> CartSummary:
        cart = self.repo.get_open_cart(user.id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay carrito activo.")
        item = self.repo.get_item_by_product(cart.id, product_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no está en el carrito.")
        self.repo.delete_item(item)
        return self._build_summary(cart)

    def get_summary(self, user: User) -> CartSummary:
        cart = self.repo.get_open_cart(user.id)
        if not cart:
            return CartSummary(items=[], subtotal=0.0, taxes=0.0, total=0.0)
        return self._build_summary(cart)

    def checkout(self, user: User):
        order_service = OrderService(self.session)
        order, summary = order_service.create_from_cart(user)
        return {"detail": "Checkout exitoso", "order": order, "summary": summary}

    def _build_summary(self, cart: Cart) -> CartSummary:
        items = self.repo.get_items(cart.id)
        detailed_items: list[CartItemRead] = []
        subtotal = 0.0
        for item in items:
            product = self.product_repo.get_by_id(item.product_id)
            product_name = product.name if product else "Producto eliminado"
            image_url = product.image_url if product else None
            category = product.category if product else None
            line_total = item.quantity * item.unit_price
            subtotal += line_total
            detailed_items.append(
                CartItemRead(
                    product_id=item.product_id,
                    name=product_name,
                    image_url=image_url,
                    category=category,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=line_total,
                )
            )
        taxes = round(subtotal * self.TAX_RATE, 2)
        total = round(subtotal + taxes, 2)
        return CartSummary(items=detailed_items, subtotal=subtotal, taxes=taxes, total=total)