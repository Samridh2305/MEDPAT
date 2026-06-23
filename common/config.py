import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # LLM CONFIGURATIONS
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENAI_EXTRACTION_MODEL = os.getenv("OPENAI_EXTRACTION_MODEL")

    # ML CONFIGURATIONS
    RAW_DATA_DIR = Path(os.getenv("RAW_DATA_DIR"))
    PROCESSED_DATA_DIR = Path(os.getenv("PROCESSED_DATA_DIR"))
    MODEL_DIR = Path(os.getenv("MODEL_DIR"))

    CORS_ALLOW_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True


settings = Settings()
