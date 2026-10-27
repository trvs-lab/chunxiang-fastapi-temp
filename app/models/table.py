
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel
from app.models.base_models.SMSCodeRecordBase import SMSCodeRecordBase
from app.models.base_models.UserBase import UserBase
from app.models.base_models.Todo import TodoBase

# 用户表
class User(UserBase, table=True):
    todos: list["Todo"] = Relationship(back_populates="user")

# 待办事项表
class Todo(TodoBase, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        index=True,
        nullable=False,
        description="所属用户",
    )
    user: User | None = Relationship(back_populates="todos")

# 短信发送记录
class SMSCodeRecord(SMSCodeRecordBase, table=True):
    pass
