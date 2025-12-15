export type ProjectStatus = "active" | "completed" | "on-hold";

export interface Project {
  id: string;
  title: string;
  description: string;
  status: ProjectStatus;
  client_id?: string | null;
  client_name?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectData {
  title: string;
  description: string;
  status: ProjectStatus;
  client_id?: string | null;
}

export interface UpdateProjectData {
  title?: string;
  description?: string;
  status?: ProjectStatus;
  client_id?: string | null;
}
