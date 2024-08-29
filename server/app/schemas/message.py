from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageRequest(BaseModel):
    message: str

class MessageRespond(BaseModel):
    source: str
    date: Optional[str]
    message_type: str
    summary: str