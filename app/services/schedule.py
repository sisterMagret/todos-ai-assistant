import json
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models.schedule import Todo
from app.schemas.vapi_schema import VapiRequest
from app.schemas.schedule import  TodoResponse
from app.database.models.users import User


class ScheduleService:
    """Service handling authentication-related operations."""

    @classmethod
    async def create_todo(
        cls, db: Session, data: VapiRequest
    ) -> dict:
        """Create a new todo.

        Args:
            db: Database session.
            data: request data.

        Returns:
            dict.
        """
        for tool_call in data.message.toolCalls:
            if tool_call.function.name == 'createTodo':
                args = tool_call.function.arguments
                break
        else:
            raise HTTPException(status_code=400, detail='Invalid Request')

        if isinstance(args, str):
            args = json.loads(args)
            
        user = db.query(User).filter(User.phone_number == args.get('phone_number', '').strip()).first()
        
        if not user:
            name = args.get('name', '')
            phone_number = args.get('phone_number', '')
            user = User(name=name, phone_number=phone_number)
            db.add(user)
            db.commit()
            

        title = args.get('title', '')
        description = args.get('description', '')

        todo = Todo(title=title, description=description, owner_id=user.id)

        db.add(todo)
        db.commit()

        return {
            'results': [
                {
                    'toolCallId': tool_call.id,
                    'result': 'success'
                }
            ]
        }
    
    @classmethod
    async def get_todos(cls, db: Session, data: VapiRequest) -> dict:
        for tool_call in data.message.toolCalls:
            if tool_call.function.name == 'getTodos':
                args = json.loads(tool_call.function.arguments) if isinstance(tool_call.function.arguments, str) else tool_call.function.arguments
                
                user = db.query(User).filter(
                    User.phone_number == args.get('phone_number', '').strip()
                ).first()
            
                if not user:
                    raise HTTPException(status_code=400, detail='User not found')
                    
                todos = db.query(Todo).filter(Todo.owner_id == user.id).all()
                
                # Convert to Pydantic models
                todo_responses = []
                for todo in todos:
                    todo_dict = {
                        'id': todo.id,
                        'title': todo.title,
                        'description': todo.description if todo.description else None,
                        'completed': todo.completed

                    }
                    todo_responses.append(TodoResponse(**todo_dict).model_dump())
                
                return {
                    'results': [{
                        'toolCallId': tool_call.id,
                        'result': todo_responses
                    }]
                }

    # @classmethod
    # async def complete_todo(cls, db: Session, data: VapiRequest,):
    #     for tool_call in data.message.toolCalls:
    #             if tool_call.function.name == 'completeTodo':
    #                 args = tool_call.function.arguments
    #                 break
    #     else:
    #         raise HTTPException(status_code=400, detail='Invalid Request')
        
    #     if isinstance(args, str):
    #         args = json.loads(args)

    #     user = db.query(User).filter(User.phone_number == args.get('phone_number', '').strip()).first()
        
    #     if not user:
    #         raise HTTPException(status_code=400, detail='User not found')
    #     todo_title = args.get('title')

    #     if not todo_title:
    #         raise HTTPException(status_code=400, detail='Missing To-Do ID')

    #     todo = db.query(Todo).filter(
    #             Todo.title.ilike(f"%{todo_title.strip()}%") & 
    #             (Todo.owner_id == user.id)
    #         ).first()

    #     if not todo:
    #         raise HTTPException(status_code=404, detail='Todo not found')

    #     todo.completed = True

    #     db.commit()
    #     db.refresh(todo)

    #     return {
    #         'results': [
    #             {
    #                 'toolCallId': tool_call.id,
    #                 'result': 'success'
    #             }
    #         ]
    #     }
    @classmethod
    async def complete_todo(cls, db: Session, data: VapiRequest):
        for tool_call in data.message.toolCalls:
            if tool_call.function.name == 'completeTodo':
                
                args = json.loads(tool_call.function.arguments) if isinstance(tool_call.function.arguments, str) else tool_call.function.arguments
                
                user = db.query(User).filter(
                    User.phone_number == args.get('phone_number', '').strip()
                ).first()
                
                if not user:
                    raise HTTPException(status_code=400, detail='User not found')
                
                todo_title = args.get('title')
                if not todo_title:
                    raise HTTPException(status_code=400, detail='Missing To-Do title')

                todo = db.query(Todo).filter(
                    Todo.title.ilike(f"%{todo_title.strip()}%"),
                    Todo.owner_id == user.id
                ).first()

                if not todo:
                    raise HTTPException(status_code=404, detail='Todo not found')

                # Update and commit
                todo.completed = True
                db.commit()
                db.refresh(todo)

                return {
                    'results': [{
                        'toolCallId': tool_call.id,
                        'result': 'success'
                    }]
                }
        raise HTTPException(status_code=400, detail='Invalid Request')

    @classmethod
    async def delete_todo(cls, db: Session, data: VapiRequest):
        for tool_call in data.message.toolCalls:
                if tool_call.function.name == 'deleteTodo':
                    args = tool_call.function.arguments
                    break
        else:
            raise HTTPException(status_code=400, detail='Invalid Request')

        if isinstance(args, str):
            args = json.loads(args)

        todo_title = args.get('title')
        
        user = db.query(User).filter(User.phone_number == args.get('phone_number', '').strip()).first()
        
        if not user:
            raise HTTPException(status_code=400, detail='User not found')

        if not todo_title:
            raise HTTPException(status_code=400, detail='Missing To-Do ID')

        todo = db.query(Todo).filter(
            Todo.title.ilike(f"%{todo_title.strip()}%") & 
            (Todo.owner_id == user.id)
        ).first()
        
        if not todo:
            raise HTTPException(status_code=404, detail='Todo not found')

        db.delete(todo)
        db.commit()

        return {
            'results': [
                {
                    'toolCallId': tool_call.id,
                    'result': 'success'
                }
            ]
        }

