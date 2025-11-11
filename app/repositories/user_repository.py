
from typing import Optional
from sqlmodel import Session, select
# from app.domain.interfaces.user_repository_port import IUserRepository
from app.models.user import User


class UserRepository:
    def __init__(self, session:Session):
        self.session=session
        
    def create_user(self, user:User)->User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
        
    def get_by_username(self, username:str)->Optional[User]:
        return self.session.exec(select(User).where(User.username==username)).first()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)
    
    def get_all(self) -> list[User]:
        statement = select(User)
        return self.session.exec(statement).all()
    
    def delete(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()
        return True