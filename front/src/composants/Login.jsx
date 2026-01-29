import { useState } from "react";
import { supabase } from "../supabaseClient";

function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [motDePasse, setMotDePasse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: motDePasse,
      });

      if (error) throw error;

      if (onLoginSuccess) onLoginSuccess(data.user);
    } catch (error) {
      console.error("Erreur:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-4">
      <div className="w-full max-w-sm border border-gray-200 p-6 rounded">
        <div className="mb-6">
          <h1 className="text-lg font-normal mb-1">Connexion</h1>
          <p className="text-xs text-gray-500">
            Accédez à votre espace cabinet
          </p>
        </div>

        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-xs font-normal text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="contact@cabinet.fr"
              required
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400"
            />
          </div>

          <div>
            <label className="block text-xs font-normal text-gray-700 mb-2">
              Mot de passe
            </label>
            <input
              type="password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              placeholder="••••••••"
              required
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 text-sm bg-black text-white hover:bg-gray-800 rounded disabled:opacity-50 transition-colors"
          >
            {loading ? "Connexion..." : "Se connecter"}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-gray-100">
          <p className="text-xs text-gray-500 text-center">
            Contactez-nous pour créer un compte
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
