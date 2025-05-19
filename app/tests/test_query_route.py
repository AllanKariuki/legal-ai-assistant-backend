import pytest
import uuid
from fastapi.testclient import TestClient
from app.models.database import User, Conversation, Message

def test_process_query_new_user(client, mock_llm_response, test_db):
    """Test processing a query from a new user without a user_id cookie."""
    response = client.post(
        "/api/query",
        json={"query": "What is a contract?"}
    )
    
    # Check response status and content
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "This is a mock response to: What is a contract?"
    assert "conversation_id" in data
    
    # Check that a user_id cookie was set
    assert "user_id" in response.cookies
    
    # Verify database entries
    user_id = response.cookies["user_id"]
    user = test_db.query(User).filter(User.id == user_id).first()
    assert user is not None
    
    conversation = test_db.query(Conversation).filter(Conversation.user_id == user_id).first()
    assert conversation is not None
    assert conversation.id == data["conversation_id"]
    
    messages = test_db.query(Message).filter(Message.conversation_id == conversation.id).all()
    assert len(messages) == 2  # User message and assistant response
    assert messages[0].role == "user"
    assert messages[0].content == "What is a contract?"
    assert messages[1].role == "assistant"
    assert messages[1].content == "This is a mock response to: What is a contract?"

def test_process_query_existing_user(client, mock_llm_response, test_db):
    """Test processing a query from an existing user with a user_id cookie."""
    # Create a user and set the cookie
    user_id = str(uuid.uuid4())
    user = User(id=user_id)
    test_db.add(user)
    test_db.commit()
    
    # Make request with the user_id cookie
    response = client.post(
        "/api/query",
        json={"query": "What is a tort?"},
        cookies={"user_id": user_id}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mock response to: What is a tort?"
    
    # Verify database entries
    conversation = test_db.query(Conversation).filter(Conversation.user_id == user_id).first()
    assert conversation is not None
    
    messages = test_db.query(Message).filter(Message.conversation_id == conversation.id).all()
    assert len(messages) == 2
    assert messages[0].content == "What is a tort?"

def test_process_query_existing_conversation(client, mock_llm_response, test_db):
    """Test processing a query in an existing conversation."""
    # Create user, conversation and message
    user_id = str(uuid.uuid4())
    user = User(id=user_id)
    test_db.add(user)
    
    conversation_id = str(uuid.uuid4())
    conversation = Conversation(id=conversation_id, user_id=user_id)
    test_db.add(conversation)
    
    message = Message(
        conversation_id=conversation_id,
        role="user",
        content="What is a contract?"
    )
    test_db.add(message)
    
    assistant_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content="A contract is a legally binding agreement."
    )
    test_db.add(assistant_message)
    test_db.commit()
    
    # Make request with conversation_id
    response = client.post(
        "/api/query",
        json={"query": "What about breach of contract?", "conversation_id": conversation_id},
        cookies={"user_id": user_id}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == conversation_id
    
    # Verify database entries - should now have 4 messages
    messages = test_db.query(Message).filter(Message.conversation_id == conversation_id).all()
    assert len(messages) == 4
    assert messages[2].content == "What about breach of contract?"
    assert messages[3].content == "This is a mock response to: What about breach of contract?"

def test_process_query_invalid_conversation(client, mock_llm_response, test_db):
    """Test processing a query with an invalid conversation ID."""
    # Create user
    user_id = str(uuid.uuid4())
    user = User(id=user_id)
    test_db.add(user)
    test_db.commit()
    
    # Make request with invalid conversation_id
    invalid_conversation_id = str(uuid.uuid4())
    response = client.post(
        "/api/query",
        json={"query": "What is a tort?", "conversation_id": invalid_conversation_id},
        cookies={"user_id": user_id}
    )
    
    # Should return 404 error
    assert response.status_code == 404
    assert "Conversation not found" in response.json()["detail"]

def test_process_query_error_handling(client, monkeypatch, test_db):
    """Test error handling in the query processing endpoint."""
    # Mock LLM service to raise an exception
    async def mock_error_llm_response(query):
        raise Exception("LLM service error")
    
    from app.services import llm_service
    monkeypatch.setattr(llm_service, "get_llm_response", mock_error_llm_response)
    
    # Make request
    response = client.post(
        "/api/query",
        json={"query": "What is a contract?"}
    )
    
    # Should return 500 error
    assert response.status_code == 500
    assert "LLM service error" in response.json()["detail"]
