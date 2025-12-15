import { useState, useCallback, useMemo } from "react";
import type { ReactNode } from "react";
import { STORAGE_KEYS } from "../lib/constants";
import type { User } from "../types/auth";
import { AuthContext } from "./AuthContext";

// Función helper para cargar usuario inicial
function getInitialUser(): User | null {
  const storedUser = localStorage.getItem(STORAGE_KEYS.USER);
  if (storedUser) {
    try {
      return JSON.parse(storedUser);
    } catch (error) {
      console.error("Error parsing user from storage:", error);
      localStorage.removeItem(STORAGE_KEYS.USER);
      return null;
    }
  }
  return null;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<User | null>(getInitialUser);
  const [isLoading] = useState(false);

  const setUser = useCallback((newUser: User | null) => {
    setUserState(newUser);
    if (newUser) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(newUser));
    } else {
      localStorage.removeItem(STORAGE_KEYS.USER);
    }
  }, []);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      setUser,
    }),
    [user, isLoading, setUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
