import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { LoginForm } from "../features/auth/components/LoginForm";

export function LoginPage() {
  const { isAuthenticated, user } = useAuth();

  if (isAuthenticated && user) {
    return (
      <Navigate
        to={user.role === "admin" ? "/admin/dashboard" : "/client/dashboard"}
        replace
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="flex-1 flex items-center justify-center px-4">
        <LoginForm />
      </div>
    </div>
  );
}
