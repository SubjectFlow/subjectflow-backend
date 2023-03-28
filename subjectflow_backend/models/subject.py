from __future__ import annotations
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field
from subjectflow_backend.models.pyObjectId import PyObjectId
from subjectflow_backend.models.code import Code
from bson import ObjectId


class Subject(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    code: Code
    reqOptions: List[Req] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


Req = List[str | PyObjectId]


class UpdateSubject(BaseModel):
    reqOptions: List[Req]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


Subject.update_forward_refs()
