import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchApi } from "./client";
import type { Comment, CreateCommentData } from "../types/comment";

// Get comments for a project
export function useComments(projectId: string) {
  return useQuery({
    queryKey: ["comments", projectId],
    queryFn: async (): Promise<Comment[]> => {
      return fetchApi<Comment[]>(`/projects/${projectId}/comments`);
    },
    enabled: !!projectId,
  });
}

// Create comment
export function useCreateComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateCommentData): Promise<Comment> => {
      return fetchApi<Comment>(`/projects/${data.projectId}/comments`, {
        method: "POST",
        body: JSON.stringify({ content: data.content }),
      });
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["comments", variables.projectId],
      });
    },
  });
}
