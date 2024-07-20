from pydantic import BaseModel
from typing import Optional, List

class QueryInput(BaseModel):
    input: str

class DocumentInfo(BaseModel):
    source: str
    row: Optional[int] = None
    page: Optional[int] = None
    relevance_score: float

class DocumentSummary(BaseModel):
    filename: str
    summary: Optional[str] = None
    keywords: List[str]
    classification: str
    
class QueryOutput(BaseModel):
    message: str
    documents: List[DocumentInfo]
    info: List[DocumentSummary]