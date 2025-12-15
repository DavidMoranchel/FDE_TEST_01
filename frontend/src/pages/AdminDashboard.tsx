import { Header } from "../components/layout/Header";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "../components/ui/Card";
import { useProjects } from "../api/projects";
import { Loading } from "../components/shared/Loading";
import { Error } from "../components/shared/Error";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import type { ProjectStatus } from "../types/project";

export function AdminDashboard() {
  const { data: projects, isLoading, error, refetch } = useProjects();

  if (isLoading) return <Loading />;
  if (error)
    return (
      <Error message="Failed to load projects" onRetry={() => refetch()} />
    );

  const projectsByStatus = (status: ProjectStatus) =>
    projects?.filter((p) => p.status === status) || [];

  const stats = {
    active: projectsByStatus("active").length,
    completed: projectsByStatus("completed").length,
    onHold: projectsByStatus("on-hold").length,
    total: projects?.length || 0,
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <Link to="/admin/projects/new">
            <Button>New Project</Button>
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-gray-600">Total</div>
              <div className="text-2xl font-bold mt-1">{stats.total}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-gray-600">Active</div>
              <div className="text-2xl font-bold mt-1">{stats.active}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-gray-600">Completed</div>
              <div className="text-2xl font-bold mt-1">{stats.completed}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-gray-600">On Hold</div>
              <div className="text-2xl font-bold mt-1">{stats.onHold}</div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Recent Projects</CardTitle>
          </CardHeader>
          <CardContent>
            {projects && projects.length > 0 ? (
              <div className="space-y-2">
                {projects.slice(0, 5).map((project) => (
                  <div
                    key={project.id}
                    className="flex items-center justify-between p-3 border border-gray-300"
                  >
                    <div>
                      <Link
                        to={`/admin/projects/${project.id}`}
                        className="font-medium hover:underline"
                      >
                        {project.title}
                      </Link>
                      <p className="text-sm text-gray-600 mt-1">
                        {project.description}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs border border-gray-300 px-2 py-0.5">
                          {project.status}
                        </span>
                        {project.client_name && (
                          <span className="text-xs text-gray-500">
                            Client: {project.client_name}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center py-8 text-gray-500">No projects yet</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
