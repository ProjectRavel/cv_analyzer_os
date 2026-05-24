import os
import time
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from starlette.concurrency import run_in_threadpool
from app.common.responses.response_model import ResponseModel
from app.lib.utils.cv_analyzer import CVRatingAnalyzer, analyze_cv as analyze_cv_file

cv_router = APIRouter(
    prefix="/cv",
    tags=["cv"],
)

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)


def _save_upload_file(upload_file: UploadFile, file_path: str) -> None:
    with open(file_path, "wb") as target_file:
        shutil.copyfileobj(upload_file.file, target_file, length=1024 * 1024)


@cv_router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):

    if file is None:
        res = ResponseModel(
            status_code=400,
            message="No file uploaded",
            data={},
        )
        return res.to_dict()

    if not file.filename.lower().endswith((".pdf", ".docx")):
        res = ResponseModel(
            status_code=400,
            message="Invalid file type. Only PDF and DOCX are allowed.",
            data={},
        )
        return res.to_dict()

    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        res = ResponseModel(
            status_code=400,
            message="Invalid content type. Only application/pdf and application/vnd.openxmlformats-officedocument.wordprocessingml.document are allowed.",
            data={},
        )
        return res.to_dict()

    timestamp = int(time.time())
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{os.path.splitext(file.filename)[0]}_{timestamp}{file_extension}"

    file_path = os.path.join(UPLOADS_DIR, file_name)

    try:
        await run_in_threadpool(_save_upload_file, file, file_path)
    except Exception as e:
        res = ResponseModel(
            status_code=500, message=f"Failed to save file: {str(e)}", data={}
        )
        return res.to_dict()

    res = ResponseModel(
        status_code=200,
        message="CV uploaded successfully",
        data={"file_path": file_path},
    )
    return res.to_dict()


@cv_router.post("/analyze")
async def analyze_cv_route(file: UploadFile = File(...), prompt: str = Form("")):

    if file is None:
        res = ResponseModel(
            status_code=400,
            message="No file uploaded",
            data={},
        )
        return res.to_dict()

    if not file.filename.lower().endswith((".pdf", ".docx")):
        res = ResponseModel(
            status_code=400,
            message="Invalid file type. Only PDF and DOCX are allowed.",
            data={},
        )
        return res.to_dict()

    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        res = ResponseModel(
            status_code=400,
            message="Invalid content type. Only application/pdf and application/vnd.openxmlformats-officedocument.wordprocessingml.document are allowed.",
            data={},
        )
        return res.to_dict()

    timestamp = int(time.time())
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{os.path.splitext(file.filename)[0]}_{timestamp}{file_extension}"

    file_path = os.path.join(UPLOADS_DIR, file_name)

    try:
        await run_in_threadpool(_save_upload_file, file, file_path)

        analyze_result = await run_in_threadpool(analyze_cv_file, file_path, prompt)
        res = ResponseModel(
            status_code=200,
            message="CV analyzed successfully",
            data=analyze_result.dict(),
        )

    except Exception as e:
        res = ResponseModel(
            status_code=500, message=f"Failed to save file: {str(e)}", data={}
        )
        return res.to_dict()
    return res.to_dict()
