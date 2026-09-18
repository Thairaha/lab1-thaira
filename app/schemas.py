from datetime import datetime
from pydantic import BaseModel, field_validator


class NoteBase(BaseModel):
    title: str
    content: str
    author: str

    @field_validator("title", "content", "author")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("This field cannot be empty")
        return value.strip()


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
