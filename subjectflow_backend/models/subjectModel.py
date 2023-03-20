import uuid
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field


class Subject(BaseModel):
    name: str = Field()
    code: str = Field()
