from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from subjectflow_backend.models.subject import Subject
import subjectflow_backend.api.subjectApi as subjectApi
from pydantic import BaseModel

router = APIRouter(prefix="/db")


@router.get(
    "/subject/",
    response_description="Get a subject object",
    status_code=status.HTTP_200_OK,
    response_model=Subject,
)
async def getSubject(request: Request, code: str):
    subject: Subject = subjectApi.getSubjectByCode(db=request.app.database, code=code)

    if subject is not None:
        return subject

    raise HTTPException(status_code=404, detail="Subject not found")


@router.post(
    "/subject/",
    response_description="Post a subject object",
    status_code=status.HTTP_201_CREATED,
)
async def postSubject(request: Request, subject: Subject):
    res = subjectApi.postSubject(db=request.app.database, subject=subject)

    return res
