from pydantic import BaseModel
from datetime import datetime

class MessageRequest(BaseModel):
    message: str

class MessageRespond(BaseModel):
    source: str
    date: datetime
    message_type: str
    summary: str