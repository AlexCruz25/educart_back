from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.order import CheckoutResponse
from app.security.auth_utils import require_authenticated_user
from app.services.order_service import OrderService
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=CheckoutResponse)
def create_order(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_authenticated_user),
):
    service = OrderService(session)
    order, summary = service.create_from_cart(current_user)
    return {"detail": "Orden creada correctamente", "order": order, "summary": summary}