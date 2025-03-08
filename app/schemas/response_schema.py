from baseschemas import UserBase, NoteBase
import uuid

class UserCreate(UserBase):
    password: str

class NoteCreate(NoteBase):
    pass

class UserResponse(UserBase):
    user_id: uuid.UUID
    last_update: datetime
    create_on: datetime
    notes : List["NoteResponse"] = []

    class Config:
        from_attributes = True

class NoteResponse(NoteBase):
    note_id: uuid.UUID
    last_update: datetime
    created_on: datetime
    user_id: uuid.UUID

    class Config:
        from_attributes = True