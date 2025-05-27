  
from fastapi import APIRouter, Depends, Response, HTTPException, Cookie, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import uuid

from ..db.database import get_db
from ..models.database import User, Conversation, Message
from ..models.schema import QueryRequest, QueryResponse
from ..services.llm_service import get_llm_response
from ..models.schema import ConversationSchema, MessageSchema
from typing import List

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    response: Response,
    db: Session = Depends(get_db),
    user_id: Optional[str] = Cookie(None)
):
    """
    Process a user query and return an LLM-generated response
    """
    
    # Generate or retrieve user ID
    if not user_id:
        user_id = str(uuid.uuid4())
        response_content = await handle_query(request.query, request.conversation_id, request.conversation_title, user_id, db)
        # Set cookie in response header
        response.set_cookie(key="user_id", value=user_id, httponly=True, secure=True, samesite="none", max_age=31536000)  # 1 year
        response_content.cookie = {"user_id": user_id}
        return response_content
    else:
        return await handle_query(request.query, request.conversation_id, request.conversation_title, user_id, db)

async def handle_query(query: str, conversation_id: str, conversation_title: str, user_id: str, db: Session):
    try:
        # Check if user exists, create if not
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            db.add(user)
            db.commit()
                    
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()

            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            
            #Update the conversation with the conversation title if it exists
            if conversation_title and conversation.title != conversation_title:
                conversation.title = conversation_title
                conversation.updated_at = datetime.utcnow()
                db.commit()
        else:
            conversation = Conversation(
                user_id=user_id,
                title=conversation_title,
                )
            db.add(conversation)
            db.commit()
        
        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=query
        )
        db.add(user_message)
        db.commit()
        
        # Get LLM response
        llm_response = await get_llm_response(query)
        
        # Store assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="ai",
            content=llm_response
        )
        db.add(assistant_message)
        db.commit()
        
        return QueryResponse(
            response=llm_response,
            conversation_id=conversation.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=List[ConversationSchema])
async def get_conversations(
    request: Request,
    user_id: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not user_id:
        return []
    try:
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).all()
    
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(
    conversation_id: str,
    user_id: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required")
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation
