import { Header } from "../components/layout/Header";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "../components/ui/Card";
import { useClientProjects } from "../api/projects";
import { Loading } from "../components/shared/Loading";
import { Error } from "../components/shared/Error";
import { Link } from "react-router-dom";

export function ClientDashboard() {
  const { data: projects, isLoading, error, refetch } = useClientProjects();

  if (isLoading) return <Loading />;
  if (error)
    return (
      <Error message="Failed to load projects" onRetry={() => refetch()} />
    );

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold mb-6">My Projects</h1>

        {projects && projects.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {projects.map((project) => (
              <Card key={project.id}>
                <CardHeader>
                  <CardTitle>
                    <Link
                      to={`/client/projects/${project.id}`}
                      className="hover:underline"
                    >
                      {project.title}
                    </Link>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                    {project.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs border border-gray-300 px-2 py-0.5">
                      {project.status}
                    </span>
                    <span className="text-xs text-gray-500">
                      {project.updated_at
                        ? new Date(project.updated_at).toLocaleDateString()
                        : "—"}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-500">No projects assigned yet</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
