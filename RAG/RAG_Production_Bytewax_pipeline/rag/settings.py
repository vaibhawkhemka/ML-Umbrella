from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))

    EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    CROSS_ENCODER_MODEL_ID: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    EMBEDDING_MODEL_MAX_INPUT_LENGTH: int = 256
    EMBEDDING_SIZE: int = 384
    EMBEDDING_MODEL_DEVICE: str = "cpu"
    #VECTOR_DB_OUTPUT_COLLECTION_NAME: str = ""
    VECTOR_DB_OUTPUT_INDEX_NAME: str = 'veritusrag'

    # Variables loaded from .env file
    PINECONE_URL: str = "localhost:6333"
    PINECONE_API_KEY: Optional[str] = '1c4787e9-eb8c-4252-8b8c-f0a03a77ab8a'


settings = AppSettings()