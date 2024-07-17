from pydantic import BaseModel
from typing import Optional, List

class CultQueryInput(BaseModel):
    input: str

class CultQueryOutput(BaseModel):
    message: str
    actions: Optional[List[dict]] = None