import uuid
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field
from subject import Subject


class ReqCriteria(BaseModel):
    criterion: Tuple[str, Subject]
