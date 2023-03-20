from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from subjectflow_backend.models.subject import Subject
from pydantic import BaseModel

router = APIRouter(prefix="/db")


@router.post(
    "/get-subject",
    response_description="Get a subject object",
    status_code=status.HTTP_200_OK,
    response_model=Subject,
)
async def get_subject(request: Request, subject_code: str = Body()):
    subject = request.app.database["subjects"].find_one({"code": subject_code})

    return subject
