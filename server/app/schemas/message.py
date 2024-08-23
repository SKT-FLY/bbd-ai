from pydantic import BaseModel

class MessageRequest(BaseModel):
    message: str


class MessageRespond(BaseModel):
    source: str
    date: str
    message_type: str
    reason: str
    summary: str