from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from subjectflow_backend.models.subject import Subject, ReqCriteria
from pydantic import BaseModel

router = APIRouter(prefix="/db")


@router.get(
    "/subject/",
    response_description="Get a subject object",
    status_code=status.HTTP_200_OK,
    response_model=Subject,
)
async def get_subject(request: Request, code: str):
    subject: Subject = request.app.database["subjects"].find_one({"code": code})

    if subject is not None:
        return subject

    raise HTTPException(status_code=404, detail="Subject not found")


@router.post(
    "/subject/",
    response_description="Post a subject object",
    status_code=status.HTTP_201_CREATED,
)
async def post_subject(request: Request, subject: Subject):
    request.app.database["subjects"].insert_one(jsonable_encoder(subject))
