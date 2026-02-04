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
    <div>
      {/* <h2>Profil linkedin</h2>*/}
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email Linkedin"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password Linkedin"
      />
      <button onClick={handleSignup}>Signup</button>
      {error && <p>{error}</p>}
      {success && (
        <p className="text-xs text-green-600 font-medium">
          Profil LinkedIn mis à jour avec succès !
        </p>
      )}
    </div>
  );
}
