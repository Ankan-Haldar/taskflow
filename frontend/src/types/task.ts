export type Priority = "Low" | "Medium" | "High";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  priority: Priority;
  column_id: number;
  created_at: string;
}

export interface Column {
  id: number;
  name: string;
  position: number;
  tasks: Task[];
}

export interface Board {
  id: number;
  name: string;
  columns: Column[];
}
