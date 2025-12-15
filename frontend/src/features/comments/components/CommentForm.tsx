import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useCreateComment } from "../../../api/comments";
import { Button } from "../../../components/ui/Button";

const commentSchema = z.object({
  content: z.string().min(1, "Comment cannot be empty"),
});

type CommentFormData = z.infer<typeof commentSchema>;

interface CommentFormProps {
  projectId: string;
}

export function CommentForm({ projectId }: CommentFormProps) {
  const createMutation = useCreateComment();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CommentFormData>({
    resolver: zodResolver(commentSchema),
  });

  const onSubmit = async (data: CommentFormData) => {
    try {
      await createMutation.mutateAsync({
        projectId,
        content: data.content,
      });
      reset();
    } catch (error) {
      console.error("Failed to create comment:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Add a comment
        </label>
        <textarea
          className={`block w-full rounded-lg border ${
            errors.content
              ? "border-red-300 focus:border-red-500 focus:ring-red-500"
              : "border-gray-300 focus:border-blue-500 focus:ring-blue-500"
          } px-4 py-2 focus:outline-none focus:ring-2`}
          rows={3}
          placeholder="Write your comment..."
          {...register("content")}
        />
        {errors.content && (
          <p className="mt-1 text-sm text-red-600">{errors.content.message}</p>
        )}
      </div>

      <Button type="submit" isLoading={createMutation.isPending}>
        Post Comment
      </Button>
    </form>
  );
}
