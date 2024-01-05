from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    author: Optional[str] = None