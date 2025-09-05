from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PhotoResponse(BaseModel):
    url: str
    uploaded_at: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
