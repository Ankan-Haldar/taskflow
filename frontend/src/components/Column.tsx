import type { Column as ColumnType, Task } from "../types/task";
import TaskCard from "./TaskCard";

interface Props {
  column: ColumnType;
  columns: ColumnType[];
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  onMove: (task: Task, columnId: number) => void;
}

export default function Column({
  column,
  columns,
  onEdit,
  onDelete,
  onMove,
}: Props) {
  return (
    <section className="column">
      <div className="column-header">
        <div>
          <h2>{column.name}</h2>
          <span>{column.tasks.length} task{column.tasks.length !== 1 ? "s" : ""}</span>
        </div>
      </div>

      <div className="task-list">
        {column.tasks.length === 0 ? (
          <div className="empty-column">No tasks here.</div>
        ) : (
          column.tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              columns={columns}
              onEdit={onEdit}
              onDelete={onDelete}
              onMove={onMove}
            />
          ))
        )}
      </div>
    </section>
  );
}
