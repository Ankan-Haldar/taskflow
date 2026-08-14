from app.models import Board, Column, Task


def create_board(db):
    board = Board(name="Test Board")
    todo = Column(name="To Do", position=1)
    progress = Column(name="In Progress", position=2)
    board.columns = [todo, progress]
    db.add(board)
    db.commit()
    db.refresh(board)
    return board, todo, progress


def test_creating_task_without_title_fails(client, db):
    _, todo, _ = create_board(db)

    response = client.post(
        "/api/tasks",
        json={
            "title": "   ",
            "description": "Invalid task",
            "priority": "High",
            "column_id": todo.id,
        },
    )

    assert response.status_code == 422


def test_moving_task_updates_column(client, db):
    _, todo, progress = create_board(db)

    task = Task(
        title="Move me",
        priority="Medium",
        column_id=todo.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    response = client.patch(
        f"/api/tasks/{task.id}/move",
        json={"column_id": progress.id},
    )

    assert response.status_code == 200
    assert response.json()["column_id"] == progress.id

    db.refresh(task)
    assert task.column_id == progress.id
