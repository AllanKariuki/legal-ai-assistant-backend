from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    cookie: Optional[dict] = None

class MessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class ConversationSchema(BaseModel):
    id: str
    title: Optional[str]
    created_at: datetime
    messages: List[MessageSchema]
    
    class Config:
        orm_mode = True
