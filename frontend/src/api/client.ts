import { QueryClient } from "@tanstack/react-query";
import { API_BASE_URL, STORAGE_KEYS } from "../lib/constants";
import type { ApiError } from "../types/api";

// Fetch wrapper con manejo de errores y token
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    if (headers instanceof Headers) {
      headers.set("Authorization", `Bearer ${token}`);
    } else if (Array.isArray(headers)) {
      headers.push(["Authorization", `Bearer ${token}`]);
    } else {
      (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      message: response.statusText || "An error occurred",
      statusCode: response.status,
    }));

    // Si el token es inválido, limpiar y redirigir
    if (response.status === 401) {
      localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
      window.location.href = "/login";
    }

    throw error;
  }

  return response.json();
}

// Query Client configurado
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutos
      retry: 1,
    },
  },
});

export { fetchApi };
