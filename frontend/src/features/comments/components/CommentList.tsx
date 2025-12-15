import { useComments } from "../../../api/comments";
import { Loading } from "../../../components/shared/Loading";
import { Error } from "../../../components/shared/Error";
import { formatDateTime } from "../../../lib/utils";

interface CommentListProps {
  projectId: string;
}

export function CommentList({ projectId }: CommentListProps) {
  const { data: comments, isLoading, error, refetch } = useComments(projectId);

  if (isLoading) return <Loading />;
  if (error)
    return (
      <Error message="Failed to load comments" onRetry={() => refetch()} />
    );

  if (!comments || comments.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No comments yet. Be the first to comment!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {comments.map((comment) => (
        <div
          key={comment.id}
          className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
        >
          <div className="flex items-start justify-between mb-2">
            <div>
              <span className="font-medium text-gray-900">
                {comment.user_name}
              </span>
              <span className="text-sm text-gray-500 ml-2">
                {formatDateTime(comment.created_at)}
              </span>
            </div>
          </div>
          <p className="text-gray-700 whitespace-pre-wrap">{comment.content}</p>
        </div>
      ))}
    </div>
  );
}
