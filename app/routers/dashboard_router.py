from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.dashboard import DashboardResponse
from app.security.auth_utils import require_admin
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    session: Session = Depends(get_session),
    current_user=Depends(require_admin),
):
    service = DashboardService(session)
    return service.get_dashboard()