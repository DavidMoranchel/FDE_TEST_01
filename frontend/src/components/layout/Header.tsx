import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { logout } from "../../api/auth";
import { Button } from "../ui/Button";

export function Header() {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <header className="bg-white border-b border-gray-300">
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <Link
            to={
              user?.role === "admin" ? "/admin/dashboard" : "/client/dashboard"
            }
            className="text-lg font-bold"
          >
            Portal
          </Link>

          <nav className="flex items-center gap-4">
            <Link
              to={
                user?.role === "admin"
                  ? "/admin/dashboard"
                  : "/client/dashboard"
              }
            >
              Dashboard
            </Link>
            {user?.role === "admin" && (
              <Link to="/admin/projects">Projects</Link>
            )}
            <Link to="/profile">Profile</Link>
            <span className="text-sm">{user?.name}</span>
            <span className="text-xs px-2 py-1 border border-gray-300">
              {user?.role}
            </span>
            <Button variant="outline" size="sm" onClick={handleLogout}>
              Logout
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
}
