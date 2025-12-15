import { Header } from "../components/layout/Header";
import { Card, CardContent } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { useProjects, useDeleteProject } from "../api/projects";
import { Loading } from "../components/shared/Loading";
import { Error } from "../components/shared/Error";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export function AdminProjectsList() {
  const navigate = useNavigate();
  const { data: projects, isLoading, error, refetch } = useProjects();
  const deleteMutation = useDeleteProject();

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this project?")) {
      try {
        await deleteMutation.mutateAsync(id);
      } catch (error) {
        console.error("Failed to delete project:", error);
      }
    }
  };

  if (isLoading) return <Loading />;
  if (error)
    return (
      <Error message="Failed to load projects" onRetry={() => refetch()} />
    );

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Projects</h1>
          <Link to="/admin/projects/new">
            <Button>New Project</Button>
          </Link>
        </div>

        <Card>
          <CardContent className="pt-6">
            {projects && projects.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Title
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Client
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Updated
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {projects.map((project) => (
                      <tr key={project.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Link
                            to={`/admin/projects/${project.id}`}
                            className="font-medium hover:underline"
                          >
                            {project.title}
                          </Link>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="text-xs border border-gray-300 px-2 py-1">
                            {project.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {project.client_name || "—"}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {project.updated_at
                            ? new Date(project.updated_at).toLocaleDateString()
                            : "—"}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <div className="flex justify-end gap-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() =>
                                navigate(`/admin/projects/${project.id}/edit`)
                              }
                            >
                              Edit
                            </Button>
                            <Button
                              variant="danger"
                              size="sm"
                              onClick={() => handleDelete(project.id)}
                              isLoading={deleteMutation.isPending}
                            >
                              Delete
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 mb-4">No projects yet</p>
                <Link to="/admin/projects/new">
                  <Button>Create First Project</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
