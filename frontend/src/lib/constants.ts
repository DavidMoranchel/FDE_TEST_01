export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:3000/api";

export const STORAGE_KEYS = {
  AUTH_TOKEN: "auth_token",
  USER: "user",
} as const;

export const ROUTES = {
  LOGIN: "/login",
  REGISTER: "/register",
  DASHBOARD: "/dashboard",
  ADMIN_DASHBOARD: "/admin/dashboard",
  ADMIN_PROJECTS: "/admin/projects",
  ADMIN_PROJECT_NEW: "/admin/projects/new",
  ADMIN_PROJECT_DETAIL: (id: string) => `/admin/projects/${id}`,
  ADMIN_PROJECT_EDIT: (id: string) => `/admin/projects/${id}/edit`,
  CLIENT_DASHBOARD: "/client/dashboard",
  CLIENT_PROJECT_DETAIL: (id: string) => `/client/projects/${id}`,
  PROFILE: "/profile",
} as const;
