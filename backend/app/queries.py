from sqlalchemy import text
from sqlalchemy.orm import Session


def get_task_counts_per_column(
    db: Session,
    board_id: int
) -> list[dict]:

    query = text("""
        SELECT
            c.id,
            c.name,
            COUNT(t.id) AS task_count

        FROM columns c

        LEFT JOIN tasks t
            ON t.column_id = c.id

        WHERE c.board_id = :board_id

        GROUP BY
            c.id,
            c.name,
            c.position

        ORDER BY c.position
    """)

    result = db.execute(
        query,
        {
            "board_id": board_id
        }
    )

    rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_tasks_by_priority(
    db: Session,
    priority: str
) -> list[dict]:

    query = text("""
        SELECT
            t.id,
            t.title,
            t.description,
            t.priority,
            t.created_at,
            t.column_id

        FROM tasks t

        WHERE t.priority = :priority

        ORDER BY t.created_at DESC
    """)

    result = db.execute(
        query,
        {
            "priority": priority
        }
    )

    rows = result.mappings().all()

    return [dict(row) for row in rows]