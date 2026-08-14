from app.models import Board, Column, Task
from app.queries import (
    get_task_counts_per_column,
    get_tasks_by_priority,
)


# ------------------------------------------------
# Test task count per column query
# ------------------------------------------------

def test_task_count_query_returns_expected_rows(
    db
):

    board = Board(
        name="Query Board"
    )


    todo = Column(
        name="To Do",
        position=1
    )


    done = Column(
        name="Done",
        position=2
    )


    board.columns = [
        todo,
        done
    ]


    db.add(board)

    db.flush()


    # Two tasks in To Do
    task_one = Task(
        title="Task One",
        priority="High",
        column_id=todo.id
    )


    task_two = Task(
        title="Task Two",
        priority="Low",
        column_id=todo.id
    )


    # One task in Done
    task_three = Task(
        title="Task Three",
        priority="High",
        column_id=done.id
    )


    db.add_all([
        task_one,
        task_two,
        task_three
    ])


    db.commit()


    # Execute actual SQL query
    rows = get_task_counts_per_column(
        db,
        board.id
    )


    assert rows == [
        {
            "id": todo.id,
            "name": "To Do",
            "task_count": 2
        },
        {
            "id": done.id,
            "name": "Done",
            "task_count": 1
        }
    ]


# ------------------------------------------------
# Test priority query
# ------------------------------------------------

def test_priority_query_returns_newest_first(
    db
):

    board = Board(
        name="Priority Board"
    )


    todo = Column(
        name="To Do",
        position=1
    )


    board.columns = [
        todo
    ]


    db.add(board)

    db.flush()


    older = Task(
        title="Older High Task",
        priority="High",
        column_id=todo.id
    )


    newer = Task(
        title="Newer High Task",
        priority="High",
        column_id=todo.id
    )


    low_priority = Task(
        title="Low Task",
        priority="Low",
        column_id=todo.id
    )


    db.add_all([
        older,
        newer,
        low_priority
    ])


    db.commit()


    # Make older task actually older
    from datetime import timedelta

    older.created_at = (
        newer.created_at - timedelta(days=1)
    )

    db.commit()


    rows = get_tasks_by_priority(
        db,
        "High"
    )


    titles = [
        row["title"]
        for row in rows
    ]


    assert titles == [
        "Newer High Task",
        "Older High Task"
    ]