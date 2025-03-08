from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    user_name : str
    user_email : EmailStr

class NoteBase(BaseModel):
    note_title : str
    note_content : str

class UserLogin(BaseModel):
    user_email : EmailStr
    password: str