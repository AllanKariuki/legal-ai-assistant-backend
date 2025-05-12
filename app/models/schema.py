from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="User query")

class QueryResponse(BaseModel):
    response: str = Field(..., description="LLM generated response")

class MessageHistory(BaseModel):
    messages: list = Field(default_factory=list, description="Message History")
    