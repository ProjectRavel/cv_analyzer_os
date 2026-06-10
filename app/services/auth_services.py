from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models.user import User
from schemas.user import RegisterRequest
from repositories.user_repository import UserRepository

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

class AuthService:
    
    @staticmethod
    def register(db: Session, request: RegisterRequest):
        # Check if email already exists
        existing_user = UserRepository.find_by_email(db, request.email)
        if existing_user:
            raise ValueError("Email already registered")

        # Check if username already exists
        existing_user = UserRepository.find_by_username(db, request.username)
        if existing_user:
            raise ValueError("Username already taken")

        # Hash the password
        hashed_password = pwd_context.hash(request.password)

        # Create new user
        new_user = User(
            username=request.username,
            email=request.email,
            name=request.name,
            password=hashed_password
        )

        return UserRepository.create(db, new_user)