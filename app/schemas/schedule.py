from pydantic import BaseModel, ConfigDict


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

    model_config = ConfigDict(from_attributes=True)
