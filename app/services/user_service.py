
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.user import User, UserRole

# from app.domain.interfaces.user_repository_port import IUserRepository

from app.schemas.user import UserCreate, UserLogin
from app.security.auth_utils import create_access_token, hash_password, verify_password

# from passlib.context import CryptContext

# from app.repositories.user_repository_port import UserRepository
from app.schemas.user import UserRead
from app.repositories.user_repository import UserRepository

# pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session:Session):
        self.repo=UserRepository(session)
        
    def register_user(self, user_data:UserCreate)->UserRead:
        existing=self.repo.get_by_username(user_data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está registrado."
            )
        existing_email = self.repo.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )

        hashed=hash_password(user_data.password)
        role = user_data.role or UserRole.USER
        new_user=User(username=user_data.username, email=user_data.email, password_hash=hashed, role=role)
        created_user = self.repo.create_user(new_user)
        return UserRead.from_orm(created_user)
    
    def authenticate_user(self, credentials:UserLogin)->Optional[UserRead]:
        user=self.repo.get_by_username(credentials.username)
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas."
            )
        token=create_access_token({"sub":user.username})
        return token

    def demo_login(self) -> str:
        demo_username = "demo_user"
        user = self.repo.get_by_username(demo_username)
        if not user:
            demo_password = hash_password("demo")
            user = User(username=demo_username, password_hash=demo_password, role=UserRole.USER)
            self.repo.create_user(user)
        return create_access_token({"sub": user.username})
    
    
    def get_all_users(self) -> list[UserRead]:
        users = self.repo.get_all()
        return [UserRead.from_orm(u) for u in users]

    
    def delete_user(self, user_id: int) -> dict:
        deleted = self.repo.delete(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        return {"detail": "Usuario eliminado correctamente."}