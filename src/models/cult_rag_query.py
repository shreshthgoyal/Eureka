from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QueryInput(BaseModel):
    input: str

class DocumentInfo(BaseModel):
    source: str
    row: Optional[int] = None
    page: Optional[int] = None
    relevance_score: float

class DocumentSummary(BaseModel):
    filename: str
    summary: str
    keywords: List[str]
    classification: str
    
class QueryOutput(BaseModel):
    message: str
    documents: List[DocumentInfo]
    info: List[DocumentSummary]

class SelectInput(BaseModel):
    query: str
    document_title: str

class SelectOutput(BaseModel):
    message: str
    chain_instance: Any

class MessageInput(BaseModel):
    session_id: str
    query: str

class MessageOutput(BaseModel):
    response: str
    history: List[str]