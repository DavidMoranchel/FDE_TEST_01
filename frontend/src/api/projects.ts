import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchApi } from "./client";
import type {
  Project,
  CreateProjectData,
  UpdateProjectData,
} from "../types/project";

// Get all projects (Admin only)
export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: async (): Promise<Project[]> => {
      return fetchApi<Project[]>("/projects");
    },
  });
}

// Get single project
export function useProject(id: string) {
  return useQuery({
    queryKey: ["projects", id],
    queryFn: async (): Promise<Project> => {
      return fetchApi<Project>(`/projects/${id}`);
    },
    enabled: !!id,
  });
}

// Get client projects
export function useClientProjects() {
  return useQuery({
    queryKey: ["projects", "client"],
    queryFn: async (): Promise<Project[]> => {
      return fetchApi<Project[]>("/projects/my-projects");
    },
  });
}

// Create project (Admin only)
export function useCreateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateProjectData): Promise<Project> => {
      return fetchApi<Project>("/projects", {
        method: "POST",
        body: JSON.stringify(data),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}

// Update project (Admin only)
export function useUpdateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      id,
      data,
    }: {
      id: string;
      data: UpdateProjectData;
    }): Promise<Project> => {
      return fetchApi<Project>(`/projects/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      queryClient.invalidateQueries({ queryKey: ["projects", variables.id] });
    },
  });
}

// Delete project (Admin only)
export function useDeleteProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      return fetchApi<void>(`/projects/${id}`, {
        method: "DELETE",
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}
