import type { Column, Task } from "../types/task";

interface Props {
  task: Task;
  columns: Column[];
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  onMove: (task: Task, columnId: number) => void;
}

export default function TaskCard({
  task,
  columns,
  onEdit,
  onDelete,
  onMove,
}: Props) {
  return (
    <article className="task-card">
      <div className="task-top">
        <h3>{task.title}</h3>
        <span className={`priority ${task.priority.toLowerCase()}`}>
          {task.priority}
        </span>
      </div>

      {task.description && (
        <p className="description">{task.description}</p>
      )}

      <p className="created">
        Created {new Date(task.created_at).toLocaleDateString()}
      </p>

      <div className="task-actions">
        <button onClick={() => onEdit(task)}>Edit</button>
        <button className="danger" onClick={() => onDelete(task)}>
          Delete
        </button>

        <select
          value={task.column_id}
          onChange={(event) =>
            onMove(task, Number(event.target.value))
          }
          aria-label={`Move ${task.title}`}
        >
          {columns.map((column) => (
            <option key={column.id} value={column.id}>
              Move to {column.name}
            </option>
          ))}
        </select>
      </div>
    </article>
  );
}
