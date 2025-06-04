from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application configuration settings."""
    # Database
    DB_USER: str = Field(..., description="Database username")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: str = Field(..., description="Database port")
    DB_NAME: str = Field(..., description="Database name")

    # VAPI
    VAPI_API_PUBLIC_KEY: str = Field(..., description="VAPI public key")
    VAPI_API_PRIVATE_KEY: str = Field(..., description="VAPI private key")
    DEFAULT_ASSISTANT_ID: str = Field(
        ..., description="Default assistant ID"
    )
    MODEL: str = Field(..., description="AI model name")
    PhoneNumberID: str = Field(..., description="Phone number ID")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}\
    @{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "forbid"


settings = Settings()
