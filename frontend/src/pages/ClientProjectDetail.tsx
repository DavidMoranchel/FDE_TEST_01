import { useParams, Link } from "react-router-dom";
import { Header } from "../components/layout/Header";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "../components/ui/Card";
import { useProject } from "../api/projects";
import { Loading } from "../components/shared/Loading";
import { Error } from "../components/shared/Error";
import { CommentList } from "../features/comments/components/CommentList";
import { CommentForm } from "../features/comments/components/CommentForm";
import { formatDateTime } from "../lib/utils";

export function ClientProjectDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: project, isLoading, error, refetch } = useProject(id || "");

  if (isLoading) return <Loading />;
  if (error)
    return <Error message="Failed to load project" onRetry={() => refetch()} />;
  if (!project) return <Error message="Project not found" />;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="mb-6">
          <Link to="/client/dashboard" className="hover:underline">
            ← Back to Dashboard
          </Link>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>{project.title}</CardTitle>
              <span className="text-xs border border-gray-300 px-2 py-1">
                {project.status}
              </span>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 mb-4 whitespace-pre-wrap">
              {project.description}
            </p>
            <div className="text-sm text-gray-500 space-y-1">
              <p>
                <span className="font-medium">Updated:</span>{" "}
                {formatDateTime(project.updated_at)}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Comments</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <CommentForm projectId={project.id} />
              <div className="border-t border-gray-200 pt-6">
                <CommentList projectId={project.id} />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
