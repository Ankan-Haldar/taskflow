import { useEffect, useMemo, useState } from "react";
import Column from "./components/Column";
import TaskForm from "./components/TaskForm";
import {
  createTask,
  deleteTask,
  getBoard,
  moveTask,
  updateTask,
} from "./services/api";
import type { Board, Priority, Task } from "./types/task";

function App() {
  const [board, setBoard] = useState<Board | null>(null);
  const [priorityFilter, setPriorityFilter] = useState<"All" | Priority>("All");
  const [search, setSearch] = useState("");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadBoard() {
    try {
      setLoading(true);
      setError("");
      const data = await getBoard();
      setBoard(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load board.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadBoard();
  }, []);

  const visibleColumns = useMemo(() => {
    if (!board) return [];

    return board.columns.map((column) => ({
      ...column,
      tasks: column.tasks.filter((task) => {
        const priorityMatches =
          priorityFilter === "All" || task.priority === priorityFilter;
        const searchMatches = task.title
          .toLowerCase()
          .includes(search.toLowerCase());

        return priorityMatches && searchMatches;
      }),
    }));
  }, [board, priorityFilter, search]);

  async function handleCreate(data: {
    title: string;
    description: string;
    priority: Priority;
    column_id: number;
  }) {
    await createTask(data);
    await loadBoard();
  }

  async function handleUpdate(data: {
    title: string;
    description: string;
    priority: Priority;
    column_id: number;
  }) {
    if (!editingTask) return;

    await updateTask(editingTask.id, {
      title: data.title,
      description: data.description,
      priority: data.priority,
    });
    await loadBoard();
  }

  async function handleDelete(task: Task) {
    if (!window.confirm(`Delete "${task.title}"?`)) return;

    try {
      setError("");
      await deleteTask(task.id);
      await loadBoard();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task.");
    }
  }

  async function handleMove(task: Task, columnId: number) {
    if (task.column_id === columnId) return;

    try {
      setError("");
      await moveTask(task.id, columnId);
      await loadBoard();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to move task.");
    }
  }

  if (loading) {
    return <div className="center-screen">Loading TaskFlow...</div>;
  }

  if (!board) {
    return (
      <div className="center-screen">
        <div>
          <h1>TaskFlow</h1>
          <p>{error || "Unable to load the board."}</p>
          <button className="primary" onClick={loadBoard}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="app">
      <header className="topbar">
        <div>
          <p className="eyebrow">TEAM TASK BOARD</p>
          <h1>{board.name}</h1>
        </div>
        <button className="primary" onClick={() => setShowCreate(true)}>
          + New Task
        </button>
      </header>

      <section className="toolbar">
        <div className="filter-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            value={priorityFilter}
            onChange={(event) =>
              setPriorityFilter(event.target.value as "All" | Priority)
            }
          >
            <option value="All">All priorities</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <div className="search-group">
          <label htmlFor="search">Search</label>
          <input
            id="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search task title..."
          />
        </div>
      </section>

      {error && (
        <div className="error global-error">
          {error}
          <button onClick={() => setError("")}>Dismiss</button>
        </div>
      )}

      <section className="board">
        {visibleColumns.map((column) => (
          <Column
            key={column.id}
            column={column}
            columns={board.columns}
            onEdit={setEditingTask}
            onDelete={handleDelete}
            onMove={handleMove}
          />
        ))}
      </section>

      {(showCreate || editingTask) && (
        <TaskForm
          columns={board.columns}
          task={editingTask}
          onSubmit={editingTask ? handleUpdate : handleCreate}
          onClose={() => {
            setShowCreate(false);
            setEditingTask(null);
          }}
        />
      )}
    </main>
  );
}

export default App;
