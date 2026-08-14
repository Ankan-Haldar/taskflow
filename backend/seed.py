from datetime import datetime, timedelta, timezone

from app.database import Base, SessionLocal, engine
from app.models import Board, Column, Task


# Create database tables
Base.metadata.create_all(bind=engine)


db = SessionLocal()


try:

    # Check whether seed data already exists
    existing = db.query(Board).first()

    if existing:

        print("Seed data already exists.")

    else:

        # -------------------------
        # Create Board
        # -------------------------

        board = Board(
            name="TaskFlow Board"
        )


        # -------------------------
        # Create Columns
        # -------------------------

        todo = Column(
            name="To Do",
            position=1
        )

        progress = Column(
            name="In Progress",
            position=2
        )

        done = Column(
            name="Done",
            position=3
        )


        # Attach columns to board
        board.columns = [
            todo,
            progress,
            done
        ]

        db.add(board)

        db.flush()


        # -------------------------
        # Create Tasks
        # -------------------------

        now = datetime.now(timezone.utc)


        tasks = [

            Task(
                title="Set up project",
                description="Create the initial project structure.",
                priority="High",
                column_id=todo.id,
                created_at=now - timedelta(minutes=20)
            ),

            Task(
                title="Design API",
                description="Define the TaskFlow REST endpoints.",
                priority="Medium",
                column_id=todo.id,
                created_at=now - timedelta(minutes=15)
            ),

            Task(
                title="Build frontend",
                description="Implement the React board.",
                priority="High",
                column_id=progress.id,
                created_at=now - timedelta(minutes=10)
            ),

            Task(
                title="Create database schema",
                description="Add boards, columns and tasks tables.",
                priority="Low",
                column_id=done.id,
                created_at=now - timedelta(minutes=5)
            ),

            Task(
                title="Write tests",
                description="Cover validation, moving and database queries.",
                priority="Medium",
                column_id=done.id,
                created_at=now
            )

        ]


        db.add_all(tasks)

        db.commit()


        print("Seed data created successfully.")


finally:

    db.close()