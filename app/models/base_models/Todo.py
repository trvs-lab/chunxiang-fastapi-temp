from sqlmodel import SQLModel, Field
from .Base import TableBase

class TodoBase(TableBase):
    title: str = Field(
      unique=True,
      index=True,
      description="标题"
    )
    completed: bool = Field(
      default=False,
      description="是否完成"
    )
