import { useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchApi } from "./client";
import type {
  AuthResponse,
  LoginCredentials,
  RegisterData,
} from "../types/auth";
import { STORAGE_KEYS } from "../lib/constants";

// Login
export function useLogin() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (
      credentials: LoginCredentials
    ): Promise<AuthResponse> => {
      const response = await fetchApi<AuthResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials),
      });

      localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, response.token);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user));

      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
}

// Register
export function useRegister() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: RegisterData): Promise<AuthResponse> => {
      const response = await fetchApi<AuthResponse>("/auth/register", {
        method: "POST",
        body: JSON.stringify(data),
      });

      // Guardar token y usuario
      localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, response.token);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user));

      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
}

// Logout helper
export function logout() {
  localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
  localStorage.removeItem(STORAGE_KEYS.USER);
  window.location.href = "/login";
}
