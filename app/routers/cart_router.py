from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartSummary
from app.schemas.order import CheckoutResponse
from app.security.auth_utils import require_authenticated_user
from app.services.cart_service import CartService
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/items", response_model=CartSummary)
def add_to_cart(
    payload: CartItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_authenticated_user),
):
    service = CartService(session)
    return service.add_item(current_user, payload)


@router.put("/items/{product_id}", response_model=CartSummary)
def update_cart_item(
    product_id: int,
    payload: CartItemUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_authenticated_user),
):
    service = CartService(session)
    return service.update_item(current_user, product_id, payload)


@router.delete("/items/{product_id}", response_model=CartSummary)
def remove_cart_item(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_authenticated_user),
):
    service = CartService(session)
    return service.remove_item(current_user, product_id)


@router.get("/summary", response_model=CartSummary)
def get_cart_summary(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_authenticated_user),
):
    service = CartService(session)
    return service.get_summary(current_user)


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_authenticated_user),
):
    service = CartService(session)
    return service.checkout(current_user)