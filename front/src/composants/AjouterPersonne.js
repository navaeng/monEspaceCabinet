import { useState } from "react";

function AjouterPersonne({ cabinetId }) {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("member");

  const handleAdd = async (e) => {
    e.preventDefault();

    alert(`Invitation envoyée à ${email}`);
  };

  return (
    <form onSubmit={handleAdd} className="space-y-4 p-4 border rounded">
      <h3 className="text-sm font-bold">Ajouter un collaborateur</h3>
      <input
        type="email"
        placeholder="Email du collègue"
        className="w-full p-2 border text-sm rounded"
        onChange={(e) => setEmail(e.target.value)}
      />
      <select
        className="w-full p-2 border text-sm rounded"
        onChange={(e) => setRole(e.target.value)}
      >
        <option value="member">Membre</option>
        <option value="admin">Admin</option>
      </select>
      <button className="bg-blue-600 text-white px-4 py-2 rounded text-xs">
        Ajouter
      </button>
    </form>
  );
}
export default AjouterPersonne;
