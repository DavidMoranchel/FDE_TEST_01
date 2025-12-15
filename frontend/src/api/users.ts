import { useQuery } from "@tanstack/react-query";
import { fetchApi } from "./client";

export interface Client {
  id: string;
  name: string;
  email: string;
}

export function useClients() {
  return useQuery({
    queryKey: ["clients"],
    queryFn: async (): Promise<Client[]> => {
      return fetchApi<Client[]>("/users/clients");
    },
  });
}
