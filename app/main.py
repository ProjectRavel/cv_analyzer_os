# CV ANALYZER OPENSOURCE - CREATING WITH GEMINI FLASH 3.0

from fastapi import FastAPI
from api.router.router import api_router


# routes
app = FastAPI()
app.include_router(api_router)