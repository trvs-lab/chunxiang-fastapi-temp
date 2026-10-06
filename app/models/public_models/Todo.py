
from sqlmodel import SQLModel, Field
from uuid import UUID

class TodoCreate(SQLModel):
    title: str = Field(min_length=1)
    completed: bool = False


class TodoUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    completed: bool | None = None


class TodoPublic(SQLModel):
    id: UUID
    title: str
    completed: bool
