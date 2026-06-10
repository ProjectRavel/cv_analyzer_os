# CV ANALYZER OPENSOURCE - CREATING WITH GEMINI FLASH 3.0

import sys
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from fastapi import FastAPI
from api.router.router import api_router


# routes
app = FastAPI()
app.include_router(api_router)