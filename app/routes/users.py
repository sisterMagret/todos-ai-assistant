import json
from app.schemas.vapi_schema import VapiRequest
from app.utils.exceptions import UserAlreadyExistsError
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.users import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    try:
        users = await UserService().get_users(db)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def add_user(
    request: VapiRequest, db: Session = Depends(get_db)
):
    """Endpoint for user registration."""
    try:
        for tool_call in request.message.toolCalls:
            if tool_call.function.name == 'createUser':
                args = tool_call.function.arguments
                break
        else:
            raise HTTPException(status_code=400, detail='Invalid Request')
        
        print(args, "--------args--add user-------")
        if isinstance(args, str):
            args = json.loads(args)
            

        user_data = {
            "name": args.get('name', ''),
            "phone_number": args.get('phone_number', ''),
            }
      
        
        _ = UserService.create_user(db, user_data)
        
        return {
        'results': [
            {
                'toolCallId': tool_call.id,
                'result': 'success'
            }
        ]
    }

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
   