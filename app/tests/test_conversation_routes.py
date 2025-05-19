import pytest
import uuid
from datetime import datetime, timedelta

def test_get_conversations_no_user_id(client, test_db):
    """Test getting conversations without a user_id cookie."""
    response = client.get("/api/conversations")
    
    # Should return empty list
    assert response.status_code == 200
    assert response.json() == []

def test_get_conversations(client, test_db):
    """Test getting conversations for a user."""
    # Create user and conversations
    user_id = str(uuid.uuid4())
    user = User(id=user_id)
    test_db.add(user)
    
    # Create two conversations with different timestamps
    conversation1 = Conversation(
        user_id=user_id,
        title="First Conversation",
        updated_at=datetime.utcnow() - timedelta(hours=1)
    )
    test_db.add(conversation1)
    
    conversation2 = Conversation(
        user_id=user_id,
        title="Second Conversation",
        updated_at=datetime.utcnow()
    )
    test_db.add(conversation2)
    test_db.commit()
    
    # Make request
    response = client.get(
        "/api/conversations",
        cookies={"user_id": user_id}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Should be ordered by updated_at (newest first)
    assert data[0]["id"] == conversation2.id
    assert data[0]["title"] == "Second Conversation"
    assert data[1]["id"] == conversation1.id
    assert data[1]["title"] == "First Conversation"

def test_get_conversation_detail(client, test_db):
    """Test getting details of a specific conversation."""
    # Create user, conversation and messages
    user_id = str(uuid.uuid4())
    user = User(id=user_id)
    test_db.add(user)
    
    conversation_id = str(uuid.uuid4())
    conversation = Conversation(id=conversation_id, user_id=user_id, title="Legal Questions")
    test_db.add(conversation)
    
    message1 = Message(
        conversation_id=conversation_id,
        role="user",
        content="What is a contract?"
    )
    test_db.add(message1)
    
    message2 = Message(
        conversation_id=conversation_id,
        role="assistant",
        content="A contract is a legally binding agreement."
    )
    test_db.add(message2)
    test_db.commit()
    
    # Make request
    response = client.get(
        f"/api/conversations/{conversation_id}",
        cookies={"user_id": user_id}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id
    assert data["title"] == "Legal Questions"
    assert len(data["messages"]) == 2
    assert data["messages"][0]["role"] == "user"
    assert data["messages"][0]["content"] == "What is a contract?"
    assert data["messages"][1]["role"] == "assistant"
    assert data["messages"][1]["content"] == "A contract is a legally binding agreement."

def test_get_conversation_not_found(client, test_db):
    """Test getting a conversation that doesn't exist."""
    # Create user
    user_id = str(uuid.uuid4())
    user = User(id=user_id)
    test_db.add(user)
    test_db.commit()
    
    # Make request with non-existent conversation ID
    non_existent_id = str(uuid.uuid4())
    response = client.get(
        f"/api/conversations/{non_existent_id}",
        cookies={"user_id": user_id}
    )
    
    # Should return 404
    assert response.status_code == 404
    assert "Conversation not found" in response.json()["detail"]

def test_get_conversation_unauthorized(client, test_db):
    """Test getting a conversation without a user_id cookie."""
    # Make request without user_id cookie
    conversation_id = str(uuid.uuid4())
    response = client.get(f"/api/conversations/{conversation_id}")
    
    # Should return 401
    assert response.status_code == 401
    assert "User ID required" in response.json()["detail"]

def test_get_conversation_wrong_user(client, test_db):
    """Test getting a conversation that belongs to another user."""
    # Create two users
    user1_id = str(uuid.uuid4())
    user1 = User(id=user1_id)
    test_db.add(user1)
    
    user2_id = str(uuid.uuid4())
    user2 = User(id=user2_id)
    test_db.add(user2)
    
    # Create conversation for user1
    conversation_id = str(uuid.uuid4())
    conversation = Conversation(id=conversation_id, user_id=user1_id)
    test_db.add(conversation)
    test_db.commit()
    
    # Try to access user1's conversation as user2
    response = client.get(
        f"/api/conversations/{conversation_id}",
        cookies={"user_id": user2_id}
    )
    
    # Should return 404 (not 403, to avoid leaking information)
    assert response.status_code == 404
    assert "Conversation not found" in response.json()["detail"]
