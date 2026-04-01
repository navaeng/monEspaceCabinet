import { useState } from "react";
//
//function EmailAuto() {
//  const [candidate, setCandidate] = useState("");
//  const [mail, setMail] = useState("");
//  const [notes, setNotes] = useState("");
//
//  return (
//    <div className="space-y-8">
//      {/* Section Nouveau Process */}
//      <section className="p-6 border border-blue-100 rounded-lg bg-blue-50/30">
//        <h3 className="text-sm font-semibold mb-4 flex items-center">
//          <span className="mr-2">🚀</span> Démarrer un nouveau process
//        </h3>
//        <div className="flex gap-3">
//          <input
//            type="text"
//            placeholder="Nom du candidat..."
//            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
//            onChange={(e) => setCandidate(e.target.value)}
//          />
//             <input
//            type="text"
//            placeholder="Point à mentionner dans le mail..."
//            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
//            onChange={(e) => setNotes(e.target.value)}
//          />
//            <input
//            type="text"
//            placeholder="Email du candidat..."
//            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
//            onChange={(e) => setMail(e.target.value)}
//          />
//          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-xs font-medium transition-colors">
//            Envoyer
//          </button>
//        </div>
//      </section>
//


//      {/* Section Historique */}
//      <section>
//        <h3 className="text-sm font-semibold mb-4 text-gray-700">
//          Historique des recrutements
//        </h3>
//        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
//          <table className="w-full text-left text-sm">
//            <thead className="bg-gray-50 border-b border-gray-200 text-gray-600">
//              <tr>
//                <th className="px-4 py-2 font-medium">Candidat</th>
//                <th className="px-4 py-2 font-medium">Date</th>
//                <th className="px-4 py-2 font-medium">Statut</th>
//              </tr>
//            </thead>
//            {/* <tbody className="divide-y divide-gray-100">
//              {history.map((h) => (
//                <tr key={h.id} className="hover:bg-gray-50 transition-colors">
//                  <td className="px-4 py-3 font-medium text-gray-900">
//                    {h.name}
//                  </td>
//                  <td className="px-4 py-3 text-gray-500">{h.date}</td>
//                  <td className="px-4 py-3">
//                    <span
//                      className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase ${
//                        h.status === "Recruté"
//                          ? "bg-green-100 text-green-700"
//                          : h.status === "Refusé"
//                            ? "bg-red-100 text-red-700"
//                            : "bg-blue-100 text-blue-700"
//                      }`}
//                    >
//                      {h.status}
//                    </span>
//                  </td>
//                </tr>
//              ))}
//            </tbody>*/}
//          </table>
//        </div>
//      </section>
//    </div>
//  );
//}
//export default EmailAuto;


function EmailAuto() {
  const [candidate, setCandidate] = useState("");
  const [mail, setMail] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8001/envoyer-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nom: candidate,
          email: mail,
          notes_mail: notes
        }),
      });
      if (response.ok) alert("Email envoyé !");
    } catch (error) {
      console.error("Erreur:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <section className="p-6 border border-blue-100 rounded-lg bg-blue-50/30">
        <h3 className="text-sm font-semibold mb-4 flex items-center">
          <span className="mr-2">🚀</span> Email automatisé
        </h3>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Nom du candidat..."
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setCandidate(e.target.value)}
          />
          <input
            type="text"
            placeholder="Point à mentionner..."
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setNotes(e.target.value)}
          />
          <input
            type="text"
            placeholder="Email du candidat..."
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setMail(e.target.value)}
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-xs font-medium transition-colors disabled:bg-gray-400"
          >
            {loading ? "Envoi..." : "Envoyer"}
          </button>
        </div>
      </section>
    </div>
  );
}
export default EmailAuto;