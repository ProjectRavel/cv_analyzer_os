from fastapi import APIRouter
from app.common.responses.response_model import ResponseModel

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/")
async def health_check():
    response = ResponseModel(
        status_code=200, 
        message="API is healthy", 
        data={"status": "healthy"}
    )
    return response.to_dict()   # karena ResponseModel adalah class, kita perlu mengubahnya menjadi dictionary agar bisa dikembalikan sebagai response JSON oleh FastAPI.
