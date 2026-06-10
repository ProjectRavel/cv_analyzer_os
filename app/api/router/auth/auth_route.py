from fastapi import APIRouter, Form
from common.responses.response_model import ResponseModel
from lib.utils.hash_password import hash_password, verify_password
from common.config.jwt import create_acces_token
from fastapi import Depends
from sqlalchemy.orm import Session
from database.dependencies import get_db
from schemas.user import RegisterRequest
from services.auth_services import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.post("/login")

@auth_router.post("/register")
async def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        user = AuthService.register(db, payload)
        return ResponseModel(
            status_code=201,
            message="User registered successfully",
            data={"user_id": user.id}
        ).to_dict()
    except ValueError as e:
        return ResponseModel(
            status_code=400,
            message=str(e),
            data={}
        ).to_dict()
    