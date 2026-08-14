from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Task
from ..queries import get_tasks_by_priority

from ..schemas import (
    Priority,
    TaskCreate,
    TaskMove,
    TaskResponse,
    TaskUpdate
)

from ..services.task_service import (
    create_task,
    move_task,
    update_task
)


router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"]
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201
)
def create(
    data: TaskCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_task(
            db,
            data
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )


@router.get(
    "",
    response_model=list[TaskResponse]
)
def list_tasks(
    priority: Priority | None = Query(
        default=None
    ),
    db: Session = Depends(get_db)
):

    if priority:

        return get_tasks_by_priority(
            db,
            priority
        )

    return (
        db.query(Task)
        .order_by(
            Task.created_at.desc()
        )
        .all()
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.get(
        Task,
        task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return update_task(
        db,
        task,
        data
    )


@router.delete(
    "/{task_id}",
    status_code=204
)
def delete(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.get(
        Task,
        task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()


@router.patch(
    "/{task_id}/move",
    response_model=TaskResponse
)
def move(
    task_id: int,
    data: TaskMove,
    db: Session = Depends(get_db)
):

    task = db.get(
        Task,
        task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    try:

        return move_task(
            db,
            task,
            data.column_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )