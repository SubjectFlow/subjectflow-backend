from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.models.subjectModel import Subject
from pydantic import BaseModel

router = APIRouter(prefix="/db")


class SubjectCode(BaseModel):
    code: str


@router.post(
    "/getsubject",
    response_description="Get a subject object",
    status_code=status.HTTP_200_OK,
    response_model=Subject,
)
async def get_subject(request: Request, subject_code: SubjectCode = Body()):
    code = subject_code.code
    subject = request.app.database["subjects"].find_one({"code": code})

    return subject
