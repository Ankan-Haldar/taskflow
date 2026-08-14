import type { Board, Priority, Task } from "../types/task";

const API_URL = "https://taskflow-n2lq.onrender.com";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = "Something went wrong.";
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Keep the friendly fallback message.
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export function getBoard(boardId = 1) {
  return request<Board>(`/api/boards/${boardId}`);
}

export function createTask(data: {
  title: string;
  description: string;
  priority: Priority;
  column_id: number;
}) {
  return request<Task>("/api/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateTask(
  id: number,
  data: { title: string; description: string; priority: Priority }
) {
  return request<Task>(`/api/tasks/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export function deleteTask(id: number) {
  return request<void>(`/api/tasks/${id}`, {
    method: "DELETE",
  });
}

export function moveTask(id: number, column_id: number) {
  return request<Task>(`/api/tasks/${id}/move`, {
    method: "PATCH",
    body: JSON.stringify({ column_id }),
  });
}
