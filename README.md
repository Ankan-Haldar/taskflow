# TaskFlow

A small full-stack task board built for the TaskFlow take-home assignment.

## Stack

- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- ORM: SQLAlchemy
- Database: SQLite
- Validation: Pydantic v2
- Tests: Pytest

## Features

- View a board with columns and tasks
- Create, edit, and delete tasks
- Move tasks between columns
- Filter tasks by priority
- Text search by title
- Task count per column
- Backend validation for empty titles
- Friendly frontend error handling
- Seed data
- Required relational schema
- Required SQL queries
- Backend tests

## Project structure

```text
taskflow/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── queries.py
│   ├── tests/
│   ├── schema.sql
│   ├── seed.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## Backend setup

```bash
cd backend

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create seed data:

```bash
python seed.py
```

Start API:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Tests

From `backend`:

```bash
pytest -q
```

## Database

The application uses SQLite so no separate database server is required.

The database schema is also included as:

```text
backend/schema.sql
```

Required relational constraints include:

- Primary key on every table
- `columns.board_id` → `boards.id`
- `tasks.column_id` → `columns.id`
- `NOT NULL` on required fields

## Required SQL queries

### 1. Count tasks per column

```sql
SELECT
    c.id,
    c.name,
    COUNT(t.id) AS task_count
FROM columns c
LEFT JOIN tasks t ON t.column_id = c.id
WHERE c.board_id = :board_id
GROUP BY c.id, c.name, c.position
ORDER BY c.position;
```

### 2. Tasks by priority, newest first

```sql
SELECT
    t.id,
    t.title,
    t.description,
    t.priority,
    t.created_at,
    t.column_id
FROM tasks t
WHERE t.priority = :priority
ORDER BY t.created_at DESC;
```

These queries are executed against the database in `backend/app/queries.py`; results are not calculated by fetching every task into Python.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/boards/{board_id}` | Get board with columns/tasks |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{task_id}` | Edit task |
| DELETE | `/api/tasks/{task_id}` | Delete task |
| PATCH | `/api/tasks/{task_id}/move` | Move task |
| GET | `/api/tasks?priority=High` | Filter by priority |

## Decisions and assumptions

- A single default board is seeded because accounts, teams, and multi-board management are outside the assignment scope.
- Columns are fixed in the seed data and tasks can be moved between them.
- Moving is implemented with a column selector rather than drag-and-drop because the assignment explicitly allows a simple control.
- SQLite was chosen to make a clean clone-and-run experience possible without requiring a separate database server.
- Priority defaults to `Medium`.

## What I would improve with more time

- Drag-and-drop task movement
- Pagination for larger task collections
- Database migrations with Alembic
- More granular API/service tests
- Production deployment and CI
- Better accessibility and visual polish

## Time spent

Approximately: [fill this in before submission]

## What I learned

[Add 2–4 sentences about something you looked up or found interesting while building the project.]
