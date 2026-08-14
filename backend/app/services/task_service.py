from sqlalchemy.orm import Session

from ..models import Column, Task
from ..schemas import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    data: TaskCreate
) -> Task:

    column = db.get(
        Column,
        data.column_id
    )

    if not column:
        raise ValueError(
            "Column not found"
        )

    task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        column_id=data.column_id
    )

    db.add(task)

    db.commit()

    db.refresh(task)

    return task


def update_task(
    db: Session,
    task: Task,
    data: TaskUpdate
) -> Task:

    task.title = data.title
    task.description = data.description
    task.priority = data.priority

    db.commit()

    db.refresh(task)

    return task


def move_task(
    db: Session,
    task: Task,
    column_id: int
) -> Task:

    column = db.get(
        Column,
        column_id
    )

    if not column:
        raise ValueError(
            "Target column not found"
        )

    task.column_id = column_id

    db.commit()

    db.refresh(task)

    return task