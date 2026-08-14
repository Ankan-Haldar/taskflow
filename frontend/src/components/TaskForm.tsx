import { useEffect, useState } from "react";
import type { Column, Priority, Task } from "../types/task";

interface Props {
  columns: Column[];
  task?: Task | null;
  onSubmit: (data: {
    title: string;
    description: string;
    priority: Priority;
    column_id: number;
  }) => Promise<void>;
  onClose: () => void;
}

export default function TaskForm({
  columns,
  task,
  onSubmit,
  onClose,
}: Props) {
  const [title, setTitle] = useState(task?.title ?? "");
  const [description, setDescription] = useState(task?.description ?? "");
  const [priority, setPriority] = useState<Priority>(
    task?.priority ?? "Medium"
  );
  const [columnId, setColumnId] = useState(
    task?.column_id ?? columns[0]?.id ?? 0
  );
  const [error, setError] = useState("");

  useEffect(() => {
    setTitle(task?.title ?? "");
    setDescription(task?.description ?? "");
    setPriority(task?.priority ?? "Medium");
    setColumnId(task?.column_id ?? columns[0]?.id ?? 0);
    setError("");
  }, [task, columns]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    if (!title.trim()) {
      setError("Task title is required.");
      return;
    }

    try {
      setError("");
      await onSubmit({
        title: title.trim(),
        description: description.trim(),
        priority,
        column_id: columnId,
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task.");
    }
  }

  return (
    <div className="modal-backdrop">
      <form className="modal" onSubmit={handleSubmit}>
        <div className="modal-header">
          <h2>{task ? "Edit task" : "Create task"}</h2>
          <button type="button" className="icon-button" onClick={onClose}>
            ×
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        <label>
          Title
          <input
            autoFocus
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="e.g. Finish API integration"
          />
        </label>

        <label>
          Description
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="Optional description"
            rows={4}
          />
        </label>

        <label>
          Priority
          <select
            value={priority}
            onChange={(event) =>
              setPriority(event.target.value as Priority)
            }
          >
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>
        </label>

        {!task && (
          <label>
            Column
            <select
              value={columnId}
              onChange={(event) => setColumnId(Number(event.target.value))}
            >
              {columns.map((column) => (
                <option key={column.id} value={column.id}>
                  {column.name}
                </option>
              ))}
            </select>
          </label>
        )}

        <div className="modal-actions">
          <button type="button" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="primary">
            {task ? "Save changes" : "Create task"}
          </button>
        </div>
      </form>
    </div>
  );
}
