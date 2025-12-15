export interface Comment {
  id: string;
  project_id: string;
  user_id: string;
  user_name: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface CreateCommentData {
  projectId: string;
  content: string;
}
