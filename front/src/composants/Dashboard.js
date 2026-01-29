import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white font-sans">
      <div className="max-w-4xl mx-auto p-4 md:p-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-lg font-normal text-gray-900 mb-1">
            Tableau de bord
          </h1>
          <p className="text-xs text-gray-500">Espace cabinet de recrutement</p>
        </div>

        {/* Actions principales */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Dossier de compétences */}
          <div
            onClick={() => navigate("/dossier_competences")}
            className="border border-gray-200 rounded p-4 cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-start mb-3">
              <div className="text-gray-400 mr-3">📄</div>
              <div>
                <h3 className="text-sm font-normal mb-1">
                  Dossier de compétences
                </h3>
                <p className="text-xs text-gray-500">
                  Générez et gérez vos dossiers
                </p>
              </div>
            </div>
          </div>

          {/* Prospection */}
          <div
            onClick={() => navigate("/prospection")}
            className="border border-gray-200 rounded p-4 cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-start mb-3">
              <div className="text-gray-400 mr-3">🔍</div>
              <div>
                <h3 className="text-sm font-normal mb-1">Prospection</h3>
                <p className="text-xs text-gray-500">Gérez vos prospections</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
