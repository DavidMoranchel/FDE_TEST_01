import { createBrowserRouter, Navigate } from "react-router-dom";
import { ProtectedRoute } from "./ProtectedRoute";
import { RoleRoute } from "./RoleRoute";
import { LoginPage } from "../pages/LoginPage";
import { RegisterPage } from "../pages/RegisterPage";
import { AdminDashboard } from "../pages/AdminDashboard";
import { ClientDashboard } from "../pages/ClientDashboard";
import { AdminProjectsList } from "../pages/AdminProjectsList";
import { AdminCreateProject } from "../pages/AdminCreateProject";
import { AdminProjectDetail } from "../pages/AdminProjectDetail";
import { AdminEditProject } from "../pages/AdminEditProject";
import { ClientProjectDetail } from "../pages/ClientProjectDetail";
import { ProfilePage } from "../pages/ProfilePage";
import { NotFoundPage } from "../pages/NotFoundPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <Navigate to="/dashboard" replace />
      </ProtectedRoute>
    ),
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    path: "/dashboard",
    element: (
      <ProtectedRoute>
        <Navigate to="/admin/dashboard" replace />
      </ProtectedRoute>
    ),
  },
  {
    path: "/admin",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["admin"]}>
          <Navigate to="/admin/dashboard" replace />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/admin/dashboard",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["admin"]}>
          <AdminDashboard />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/admin/projects",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["admin"]}>
          <AdminProjectsList />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/admin/projects/new",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["admin"]}>
          <AdminCreateProject />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/admin/projects/:id",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["admin"]}>
          <AdminProjectDetail />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/admin/projects/:id/edit",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["admin"]}>
          <AdminEditProject />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/client",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["client"]}>
          <Navigate to="/client/dashboard" replace />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/client/dashboard",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["client"]}>
          <ClientDashboard />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/client/projects/:id",
    element: (
      <ProtectedRoute>
        <RoleRoute allowedRoles={["client"]}>
          <ClientProjectDetail />
        </RoleRoute>
      </ProtectedRoute>
    ),
  },
  {
    path: "/profile",
    element: (
      <ProtectedRoute>
        <ProfilePage />
      </ProtectedRoute>
    ),
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);
