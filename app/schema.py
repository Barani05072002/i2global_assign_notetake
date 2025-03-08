from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid

class UserBase(BaseModel):
    user_name : str
    user_email : EmailStr

class NoteBase(BaseModel):
    note_title : str
    note_content : str
    last_update : datetime

