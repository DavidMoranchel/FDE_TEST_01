import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate, useParams } from "react-router-dom";
import { useProject, useUpdateProject } from "../api/projects";
import { useClients } from "../api/users";
import { Header } from "../components/layout/Header";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Loading } from "../components/shared/Loading";
import { Error } from "../components/shared/Error";

const projectSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().min(1, "Description is required"),
  status: z.enum(["active", "completed", "on-hold"]),
  client_id: z.string().optional().nullable(),
});

type ProjectFormData = z.infer<typeof projectSchema>;

export function AdminEditProject() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: project, isLoading, error } = useProject(id || "");
  const updateMutation = useUpdateProject();
  const { data: clients = [], isLoading: clientsLoading } = useClients();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
  });

  // Reset form when project data loads
  useEffect(() => {
    if (project && !isLoading) {
      reset({
        title: project.title,
        description: project.description,
        status: project.status,
        client_id: project.client_id || null,
      });
    }
  }, [project, isLoading, reset]);

  const onSubmit = async (data: ProjectFormData) => {
    if (!id) return;
    try {
      await updateMutation.mutateAsync({ id, data });
      navigate(`/admin/projects/${id}`);
    } catch (error) {
      console.error("Failed to update project:", error);
    }
  };

  if (isLoading) return <Loading />;
  if (error) return <Error message="Failed to load project" />;
  if (!project) return <Error message="Project not found" />;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-3xl mx-auto px-4 py-6">
        <Card>
          <CardHeader>
            <CardTitle>Edit Project</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <Input
                label="Title"
                type="text"
                placeholder="Project title"
                error={errors.title?.message}
                {...register("title")}
              />

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  className={`block w-full rounded-lg border ${
                    errors.description
                      ? "border-red-300 focus:border-red-500 focus:ring-red-500"
                      : "border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                  } px-4 py-2 focus:outline-none focus:ring-2`}
                  rows={4}
                  placeholder="Project description"
                  {...register("description")}
                />
                {errors.description && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.description.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  className="block w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  {...register("status")}
                >
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="on-hold">On Hold</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Client (optional)
                </label>
                <select
                  className="block w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  {...register("client_id")}
                  disabled={clientsLoading}
                >
                  <option value="">No client assigned</option>
                  {clients.map((client) => (
                    <option key={client.id} value={client.id}>
                      {client.name} ({client.email})
                    </option>
                  ))}
                </select>
                {errors.client_id && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.client_id.message}
                  </p>
                )}
              </div>

              <div className="flex gap-4">
                <Button type="submit" isLoading={updateMutation.isPending}>
                  Update Project
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate(`/admin/projects/${id}`)}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
