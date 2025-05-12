from fastapi import APIRouter, HTTPException, Depends
from app.models.schema import QueryRequest, QueryResponse
from app.services.llm_service import get_llm_response

router = APIRouter()

@router.post("query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
        Process a user query and return an LLM-generated response
    """

    try:
        response = await get_llm_response(request.query)
        return QueryResponse(
            response=response,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
