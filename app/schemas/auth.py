from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    """Schema for user creation (signup)."""

    name: str = Field(
        ..., description="Full Name."
    )
    phone_number: str = Field(
        ..., description="Phone Number."
    )
