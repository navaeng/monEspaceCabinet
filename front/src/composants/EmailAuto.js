import React from "react";

function EmailAuto() {
  const steps = [
    { id: 1, name: "Alice", step: "Entretien RH", color: "bg-blue-100" },
    { id: 2, name: "Bob", step: "Test Technique", color: "bg-yellow-100" },
    { id: 3, name: "Charlie", step: "Offre envoyée", color: "bg-green-100" },
  ];

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-bold">Processus en cours</h3>
      {steps.map((s) => (
        <div
          key={s.id}
          className={`p-3 rounded border flex justify-between items-center ${s.color}`}
        >
          <span className="text-sm font-medium">{s.name}</span>
          <span className="text-xs font-semibold px-2 py-1 bg-white rounded-full shadow-sm">
            {s.step}
          </span>
        </div>
      ))}
    </div>
  );
}
export default EmailAuto;
