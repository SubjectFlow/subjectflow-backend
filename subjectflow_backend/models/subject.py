from __future__ import annotations
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field


class Subject(BaseModel):
    name: str
    code: str
    reqOptions: List[ReqCriteria] = None


class ReqCriteria(BaseModel):
    criterion: Tuple[str, Subject]


Subject.update_forward_refs()
