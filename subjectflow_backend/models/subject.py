import uuid
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field
from reqCriteria import ReqCriteria


class Subject(BaseModel):
    name: str
    code: str
    reqOptions: List[ReqCriteria] = None
