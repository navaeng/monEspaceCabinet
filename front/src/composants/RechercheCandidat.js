import React, { useState } from "react";

function RechercheCandidat() {
  const [search, setSearch] = useState("");
  const candidates = [{ id: 1, name: "", job: "Développeur React" }];

  return (
    <div className="p-4 border rounded">
      <input
        type="text"
        placeholder="Rechercher un candidat..."
        className="w-full p-2 mb-4 border text-sm rounded"
        onChange={(e) => setSearch(e.target.value)}
      />
      <div className="space-y-2">
        {candidates
          .filter((c) => c.name.toLowerCase().includes(search.toLowerCase()))
          .map((c) => (
            <div
              key={c.id}
              className="flex justify-between p-2 bg-gray-50 rounded text-sm"
            >
              <span>{c.name}</span>
              <span className="text-gray-500">{c.job}</span>
            </div>
          ))}
      </div>
    </div>
  );
}
export default RechercheCandidat;
