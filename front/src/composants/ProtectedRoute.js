import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem("supabase.auth.token");

  if (!isAuthenticated) {
    return <Navigate to="/Connexion" replace />;
  }

  return children;
};
export default ProtectedRoute;
