# from pydantic import BaseModel, Field

# class QueryRequest(BaseModel):
#     query: str = Field(..., min_length=1, max_length=1000, description="User query")

# class QueryResponse(BaseModel):
#     response: str = Field(..., description="LLM generated response")

# class MessageHistory(BaseModel):
#     messages: list = Field(default_factory=list, description="Message History")
    

from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

class MessageSchema(BaseModel):
    role: str
    content: str
    created_at: str
    
    class Config:
        orm_mode = True

class ConversationSchema(BaseModel):
    id: str
    title: Optional[str]
    created_at: str
    messages: List[MessageSchema]
    
    class Config:
        orm_mode = True
