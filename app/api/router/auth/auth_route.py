from app.common.responses.response_model import ResponseModel
from app.lib.utils.hash_password import hash_password, verify_password
from app.common.config.jwt import create_acces_token
from fastapi import APIRouter, Form

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

fake_user_db = {"email": "keza@gmail.com", "password": hash_password("kezacantik")}


@auth_router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    if email == "" or password == "":
        response = ResponseModel(
            status_code=400, message="Email and password are required", data={}
        )
        return response.to_dict()

    if email == fake_user_db["email"]:

        if not verify_password(password, fake_user_db["password"]):
            response = ResponseModel(
                status_code=401, message="Invalid email or password", data={}
            )
            return response.to_dict()

        token = create_acces_token(data={"sub": email})

        return ResponseModel(
            status_code=200,
            message="Login successful",
            data={"access_token": token, "token_type": "bearer"},
        ).to_dict()

    response = ResponseModel(
        status_code=401, message="Invalid email or password", data={}
    )
    return response.to_dict()
