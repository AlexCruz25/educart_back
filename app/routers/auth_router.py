from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.register_user(user_data)

@router.post("/login")
def login_user(credentials: UserLogin, session: Session = Depends(get_session)):
    service = UserService(session)
    token = service.authenticate_user(credentials)
    return {"access_token": token, "token_type": "bearer"}
