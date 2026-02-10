import { useState } from "react";
import Login from "./Login";

function Home() {
  const [showLogin, setShowLogin] = useState(false);

  if (showLogin) {
    return <Login onBack={() => setShowLogin(false)} />;
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero minimaliste */}
      <section className="py-20 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-normal text-gray-900 mb-4">
            Gestion simplifiée
          </h1>
          <p className="text-sm text-gray-600 mb-8 max-w-md mx-auto">
            Centralisez vos candidats, générez des dossiers professionnels,
            optimisez votre workflow.
          </p>
          <button
            onClick={() => setShowLogin(true)}
            className="text-sm px-6 py-3 bg-black text-white hover:bg-gray-800 rounded"
          >
            Accéder à mon espace
          </button>
        </div>
      </section>

      {/* Fonctionnalités essentielles */}
      <section className="py-16 border-t border-gray-100">
        <div className="max-w-4xl mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-gray-400 mb-3 text-lg">📄</div>
              <h3 className="text-sm font-normal mb-2">Dossiers complets</h3>
              <p className="text-xs text-gray-500">
                Génération automatique à partir des CV
              </p>
            </div>

            <div className="text-center">
              <div className="text-gray-400 mb-3 text-lg">⚡</div>
              <h3 className="text-sm font-normal mb-2">
                Prospection automatisé
              </h3>
              <p className="text-xs text-gray-500">
                Automatisation des tâches répétitives
              </p>
            </div>

            <div className="text-center">
              <div className="text-gray-400 mb-3 text-lg">🤖</div>
              <h3 className="text-sm font-normal mb-2">IA intégré</h3>
              <p className="text-xs text-gray-500">
                Model IA pour la pertinence des résultats
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Process simple */}
      <section className="py-16 border-t border-gray-100 bg-gray-50">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-lg font-normal text-center mb-12">
            Comment ça marche
          </h2>
          <div className="space-y-8">
            <div className="flex items-start">
              <div className="text-xs font-normal bg-white border border-gray-200 rounded-full w-6 h-6 flex items-center justify-center mr-4">
                1
              </div>
              <div>
                <h4 className="text-sm font-normal mb-1">Importez vos CV</h4>
                <p className="text-xs text-gray-500">
                  PDF ou Word, le système extrait les informations
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="text-xs font-normal bg-white border border-gray-200 rounded-full w-6 h-6 flex items-center justify-center mr-4">
                2
              </div>
              <div>
                <h4 className="text-sm font-normal mb-1">
                  Générez les dossiers
                </h4>
                <p className="text-xs text-gray-500">
                  Format standardisé, prêt pour vos clients
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="text-xs font-normal bg-white border border-gray-200 rounded-full w-6 h-6 flex items-center justify-center mr-4">
                3
              </div>
              <div>
                <h4 className="text-sm font-normal mb-1">
                  Suivez et organisez
                </h4>
                <p className="text-xs text-gray-500">
                  Tous vos candidats centralisés
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
