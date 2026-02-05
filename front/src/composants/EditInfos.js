import { useState } from "react";
import { supabase } from "../supabaseClient";

export default function EditInfos() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSignup = async () => {
    setSuccess(false);
    setError(null);
    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      if (!user) throw new Error("Aucun utilisateur connecté");

      // const user = data.user;
      if (user) {
        const { error: dbError } = await supabase.rpc(
          "upsert_linkedin_profile",
          {
            p_user_id: user.id,
            p_email: email,
            p_password: password,
          },
        );
        if (dbError) throw dbError;
        setSuccess(true);
        // .eq("id", user.id);
      }

      // const { error } = await supabase.auth.signUp({ email, password });
      // if (error) throw error;
      setError(null);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="w-56">
        <input
          type="email"
          className="w-full p-2 mb-2 text-sm border-b outline-none"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email"
        />

        <input
          type="password"
          className="w-full p-2 mb-4 text-sm border-b outline-none"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="mot de passe"
        />

        <button
          onClick={handleSignup}
          className="w-full p-2 text-sm text-white bg-gray-800"
        >
          enregistrer
        </button>

        {error && <p className="mt-2 text-xs text-red-500">{error}</p>}
        {success && <p className="mt-2 text-xs text-gray-600">sauvegardé</p>}
      </div>
    </div>
  );
}
