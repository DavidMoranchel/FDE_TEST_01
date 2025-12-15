import { RouterProvider } from "react-router-dom";
import { QueryProvider } from "./contexts/QueryProvider";
import { AuthProvider } from "./contexts/AuthContext.tsx";
import { router } from "./routes";

function App() {
  return (
    <QueryProvider>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryProvider>
  );
}

export default App;
