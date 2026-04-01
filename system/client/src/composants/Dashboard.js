import { useNavigate } from "react-router-dom";
import { supabase } from "../supabaseClient";
import { useEffect, useState } from "react";
import Header from "./Header";

function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [nom, setNom] = useState(null);
  const [cabinet, setCabinet] = useState(null);

  useEffect(() => {
    const getUserData = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      if (user) {
      }
      setUser(user);

      const { data } = await supabase
        .from("profiles")
        .select("full_name, cabinets(nom)")
        .eq("id", user.id)
        .single();

      if (data) {
        setNom(data.full_name);
        const nomcabinet = Array.isArray(data.cabinets)
          ? data.cabinets[0]?.nom
          : data.cabinets?.nom;

        setCabinet(nomcabinet);
      }
    };
    getUserData();
  }, []);

  return (
    <div className="min-h-screen bg-white font-sans">
      {/* <Header cabinetName={cabinet} />;*/}
      <div className="max-w-4xl mx-auto p-4 md:p-6">
        <div className="mb-8">
          <h1 className="text-lg font-normal text-gray-900 mb-1">
            Tableau de bord {nom ? nom : user ? user.nom : ""}
          </h1>
         
          {/* <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          >
            Déconnexion
          </button>*/}
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

          {/* Email automatisé */}
          <div
            onClick={() => navigate("/EmailAuto")}
            className="border border-gray-200 rounded p-4 cursor-pointer hover:bg-gray-50 transition-colors group"
          >
            <div className="flex items-start">
              <div className="text-xl mr-3 group-hover:scale-110 transition-transform">
                ✉️
              </div>
              <div>
                <h3 className="text-sm font-normal text-gray-900 mb-1">
                  Email automatisé
                </h3>
                <p className="text-xs text-gray-500">
                  Configurez et lancez vos campagnes d'emails
                </p>
              </div>
            </div>
          </div>
          {/* Prospection and sourcing */}
          <div
            onClick={() => navigate("/ProspectionSourcing")}
            className="border border-gray-200 rounded p-4 cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-start mb-3">
              <div className="text-gray-400 mr-3">🔍</div>
              <div>
                <h3 className="text-sm font-normal mb-1">
                  Prospection et sourcing
                </h3>
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
