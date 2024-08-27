from pydantic import BaseModel

class Settings(BaseModel):
    db_uri: str = "postgresql+asyncpg://demo:demo@localhost/demo"
