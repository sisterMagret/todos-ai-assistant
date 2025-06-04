import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app.schemas.vapi_schema import VapiRequest, Message, ToolCall, ToolCallFunction
from app.database.models.users import User
from app.database.models.schedule import Todo
import json


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(db_session):
    user = User(name="Test User", phone_number="1234567890")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_todo(db_session, test_user):
    todo = Todo(title="Test Todo", description="Test Description", owner_id=test_user.id)
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

def create_vapi_request(function_name: str, args: dict):
    return VapiRequest(
        message=Message(
            toolCalls=[
                ToolCall(
                    id="test123",
                    function=ToolCallFunction(
                        name=function_name,
                        arguments=json.dumps(args)
                    )
                )
            ]
        )
    )


# User Tests
def test_get_users_empty(db_session):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_users_with_data(db_session, test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["phone_number"] == "1234567890"

def test_create_user_success():
    request_data = create_vapi_request("createUser", {
        "name": "New User",
        "phone_number": "9876543210"
    })
    
    response = client.post("/users/", json=request_data.model_dump())
    assert response.status_code == 201
    assert response.json()["results"][0]["result"] == "success"

def test_create_user_duplicate(db_session, test_user):
    request_data = create_vapi_request("createUser", {
        "name": "Duplicate User",
        "phone_number": "1234567890"
    })
    
    response = client.post("/users/", json=request_data.model_dump())
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

# Todo Tests
def test_create_todo_success(db_session, test_user):
    request_data = create_vapi_request("createTodo", {
        "phone_number": "1234567890",
        "title": "New Todo",
        "description": "New Description"
    })
    
    response = client.post("/schedules/create_todo/", json=request_data.model_dump())
    assert response.status_code == 200
    assert response.json()["results"][0]["result"] == "success"
    
    # Verify todo was created
    todos = db_session.query(Todo).all()
    assert len(todos) == 1
    assert todos[0].title == "New Todo"

def test_create_todo_new_user():
    request_data = create_vapi_request("createTodo", {
        "phone_number": "1112223333",
        "name": "Auto Created User",
        "title": "New Todo",
        "description": "New Description"
    })
    
    response = client.post("/schedules/create_todo/", json=request_data.model_dump())
    assert response.status_code == 200
    
    # Verify both user and todo were created
    db = next(override_get_db())
    user = db.query(User).filter(User.phone_number == "1112223333").first()
    assert user is not None
    assert user.name == "Auto Created User"
    
    todo = db.query(Todo).filter(Todo.owner_id == user.id).first()
    assert todo is not None
    assert todo.title == "New Todo"

def test_get_todos_success(db_session, test_user, test_todo):
    request_data = create_vapi_request("getTodos", {
        "phone_number": "1234567890"
    })
    
    response = client.post("/schedules/get_todos/", json=request_data.model_dump())
    assert response.status_code == 200
    
    results = response.json()["results"][0]["result"]
    assert len(results) == 1
    assert results[0]["title"] == "Test Todo"
    assert results[0]["completed"] is False

def test_get_todos_user_not_found():
    request_data = create_vapi_request("getTodos", {
        "phone_number": "0000000000"
    })
    
    response = client.post("/schedules/get_todos/", json=request_data.model_dump())
    assert response.status_code == 400
    assert "User not found" in response.json()["detail"]

def test_complete_todo_success(db_session, test_user, test_todo):

    assert test_todo.completed is False
    
    request_data = create_vapi_request("completeTodo", {
        "phone_number": "1234567890",
        "title": "Test Todo"
    })
    
    response = client.post("/schedules/complete_todo/", json=request_data.model_dump())
    assert response.status_code == 200
    assert response.json()["results"][0]["result"] == "success"
    
    db_session.refresh(test_todo)
    
    db_todo = db_session.query(Todo).filter(Todo.id == test_todo.id).first()
    assert db_todo is not None
    assert db_todo.completed is True

def test_complete_todo_not_found(db_session, test_user):
    request_data = create_vapi_request("completeTodo", {
        "phone_number": "1234567890",
        "title": "Non-existent Todo"
    })
    
    response = client.post("/schedules/complete_todo/", json=request_data.model_dump())
    assert response.status_code == 404
    assert "Todo not found" in response.json()["detail"]

def test_delete_todo_success(db_session, test_user, test_todo):
    request_data = create_vapi_request("deleteTodo", {
        "phone_number": "1234567890",
        "title": "Test Todo"
    })
    
    response = client.post("/schedules/delete_todo/", json=request_data.model_dump())
    assert response.status_code == 200
   
    db_todo = db_session.query(Todo).filter(Todo.id == test_todo.id).first()
    assert db_todo is None

def test_delete_todo_not_found(db_session, test_user):
    request_data = create_vapi_request("deleteTodo", {
        "phone_number": "1234567890",
        "title": "Non-existent Todo"
    })
    
    response = client.post("/schedules/delete_todo/", json=request_data.model_dump())
    assert response.status_code == 404
    assert "Todo not found" in response.json()["detail"]

# Error cases
def test_invalid_tool_call():
    request_data = VapiRequest(
        message=Message(
            toolCalls=[
                ToolCall(
                    id="test123",
                    function=ToolCallFunction(
                        name="invalidFunction",
                        arguments=json.dumps({"key": "value"})
                    )
                )
            ]
        )
    )
    
    response = client.post("/schedules/create_todo/", json=request_data.model_dump())
    assert response.status_code == 400
    assert "Invalid Request" in response.json()["detail"]