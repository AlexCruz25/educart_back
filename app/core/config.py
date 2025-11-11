

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME:str="EduCart API"
    DATABASE_URL:str = "mysql+mysqlconnector://user:secret@localhost:3306/final"

    SECRET_KEY:str="super_secret_key"
    ALGORITHM:str="HS256"
    
settings=Settings()