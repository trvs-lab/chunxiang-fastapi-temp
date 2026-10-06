from sqlalchemy.exc import IntegrityError
from app.api.depends import SessionDep
from sqlmodel import Session, select
from uuid import UUID
from fastapi import HTTPException, APIRouter
from app.models.table import Todo
from app.models.public_models.Todo import TodoCreate, TodoUpdate, TodoPublic


def find_todo(session: Session, todo_id: UUID) -> Todo:
    todo = session.get(Todo, todo_id)

    if todo is None or todo.is_deleted:
        raise HTTPException(
            status_code=404,
            detail="待办事项不存在"
        )

    return todo

def save_todo(session: Session, todo: Todo) -> Todo:
    session.add(todo)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="保存失败：标题重复或数据违反数据库约束"
        )

    session.refresh(todo)
    return todo

router = APIRouter()

@router.post("/", response_model=TodoPublic, status_code=201)
def create_todo(data: TodoCreate, session: SessionDep):
    todo = Todo.model_validate(data)
    return save_todo(session, todo)

@router.get("/{todo_id}", response_model=TodoPublic)
def get_todo(todo_id: UUID, session: SessionDep):
    return find_todo(session, todo_id)

@router.get("/", response_model=list[TodoPublic])
def list_todos(session: SessionDep):
    statement = select(Todo).where(Todo.is_deleted == False)
    return session.exec(statement).all()

@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(todo_id: UUID, data: TodoUpdate, session: SessionDep):
    todo = find_todo(session, todo_id)
    changes = data.model_dump(exclude_unset=True)
    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="title 和 completed 可以省略，但不能设置为 null",
        )

    todo.sqlmodel_update(changes)

    return save_todo(session, todo)

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: UUID, session: SessionDep):
    todo = find_todo(session, todo_id)
    todo.is_deleted = True
    save_todo(session, todo)
    return {"ok": True}
