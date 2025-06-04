from app.schemas.vapi_schema import VapiRequest
from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.schedule import ScheduleService


router = APIRouter(prefix="/schedules", tags=["todos"])


@router.post('/create_todo/')
async def create_todo(request: VapiRequest, db: Session = Depends(get_db)):

    todo = await ScheduleService.create_todo(db, request)
    
    return todo


@router.post('/get_todos/')
async def get_todos(request: VapiRequest, db: Session = Depends(get_db)):
    
    todos = await ScheduleService.get_todos(db, request)
    
    return todos


@router.post('/complete_todo/')
async def complete_todo(request: VapiRequest, db: Session = Depends(get_db)):
    result = await ScheduleService.complete_todo(db, request)
    return result


@router.post('/delete_todo/')
async def delete_todo(request: VapiRequest, db: Session = Depends(get_db)):
    result = await ScheduleService.delete_todo(db, request)
    return result
