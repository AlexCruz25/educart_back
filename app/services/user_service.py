
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session
# from app.domain.interfaces.user_repository_port import IUserRepository
from app.models.user import User
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
        
    def register_user(self, user_data:UserCreate)->User:
        existing=self.repo.get_by_username(user_data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está registrado."
            )
        print("PASSWORD VALUE:", repr(user_data.password), type(user_data.password))

        hashed=hash_password(user_data.password)
        new_user=User(username=user_data.username, password_hash=hashed)
        return self.repo.create_user(new_user)
    
    def authenticate_user(self, credentials:UserLogin)->Optional[UserRead]:
        user=self.repo.get_by_username(credentials.username)
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas."
            )
        token=create_access_token({"sub":user.username})
        return token 
    
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