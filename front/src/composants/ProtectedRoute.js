import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

const ProtectedRoute = ({ children }) => {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      setSession(session);
      setLoading(false);
    });
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  if (loading) return <div>Chargement...</div>;

  if (!session) {
    return <Navigate to="/Connexion" replace />;
  }

  return children;
};

export default ProtectedRoute;
