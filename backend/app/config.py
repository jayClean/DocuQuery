from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    # AWS Settings
    aws_access_key_id: str 
    aws_secret_access_key: str
    aws_region: str
    s3_bucket_name: str
    elasticsearch_url: str
    openai_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
