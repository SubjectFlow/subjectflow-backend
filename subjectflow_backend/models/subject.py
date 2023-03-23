from __future__ import annotations
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field


class Subject(BaseModel):
    name: str
    code: str
    reqOptions: List[Tuple[str, Subject]] = []
