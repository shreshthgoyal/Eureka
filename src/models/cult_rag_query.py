from pydantic import BaseModel
from typing import Optional, List, Any

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
    info: Optional[List[DocumentSummary]] = None

class SelectInput(BaseModel):
    document_title: str

class SelectOutput(BaseModel):
    message: str
    session_id: Any

class MessageInput(BaseModel):
    session_id: Any
    query: str
    
class MessageOutput(BaseModel):
    response: str