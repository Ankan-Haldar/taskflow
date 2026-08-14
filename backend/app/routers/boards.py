from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Board, Column
from ..schemas import BoardResponse


router = APIRouter(
    prefix="/api/boards",
    tags=["boards"]
)


@router.get(
    "/{board_id}",
    response_model=BoardResponse
)
def get_board(
    board_id: int,
    db: Session = Depends(get_db)
):

    board = (
        db.query(Board)
        .options(
            joinedload(Board.columns)
            .joinedload(Column.tasks)
        )
        .filter(
            Board.id == board_id
        )
        .first()
    )

    if not board:
        raise HTTPException(
            status_code=404,
            detail="Board not found"
        )

    return board