from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleRequest(BaseModel):
    message: str

class ScheduleRespond(BaseModel):
    when: str
    description: str