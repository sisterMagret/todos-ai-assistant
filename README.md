# Voice AI Assistant Backend

![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![Poetry](https://img.shields.io/badge/Poetry-1.5.0-60A5FA?logo=poetry)
![SQLite](https://img.shields.io/badge/SQLite-3.42.0-003B57?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-24.0.5-2496ED?logo=docker)

Backend service for voice AI assistant with FastAPI, SQLite/PostgreSQL, and Python.

## Project Structure

.
├── app/ # Application code
│ ├── core/ # Configurations
│ ├── database/ # DB models & session
│ ├── routes/ # API endpoints
│ ├── schemas/ # Pydantic models
│ ├── services/ # Business logic
│ ├── tests/ # Test cases
│ ├── utils/ # Helpers & exceptions
│ └── main.py # FastAPI app


## Quick Start

### Prerequisites
- Python 3.13+
- Poetry 1.5+
- SQLite3 (or PostgreSQL)

### Installation

1. **Clone repository**:
```bash
    git clone https://github.com/sisterMagret/todos-ai-assistant.git
    cd todos-ai-assistant
    poetry install
    cp .env.example .env


    poetry run uvicorn app.main:app --reload
```
    
### Access docs at:

Swagger UI: http://localhost:8000/

Redoc: http://localhost:8000/redoc


### Testing
poetry run pytest --cov=app --cov-report=term-missing --cov-report=html


### API Endpoints

POST /schedules/create_todo	Create new todo item
POST /schedules/get_todos	List all todos
POST /schedules/delete_todo	delete todo
POST /schedules/complete_todo	mark todo as complete
POST /users/	User management
