import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";

function Prospection() {
  const [intitule, setIntitule] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  // const [currentStatus, setCurrentStatus] = useState("");
  const [prospection, setProspection] = useState([]);
  // const [expandedProspection, setExpandedProspection] = useState(null);
  // const [statusMessage, setStatusMessage] = useState("");
  const [itemToDelete, setItemToDelete] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeId, setActiveId] = useState(null);
  const [mode, setMode] = useState("");
  const [details, setDetails] = useState("");
  const [offre, setOffre] = useState("");

  const [statusLogs, setStatusLogs] = useState(() => {
    const saved = localStorage.getItem("prospection_logs");
    return saved ? JSON.parse(saved) : [];
  });

  const FetchProspection = async () => {
    try {
      const headers = await getAuthHeaders();
      const res = await fetch(
        "http://localhost:8000/backend/prospection/list",
        {
          method: "GET",
          headers,
        },
      );
      const data = await res.json();
      console.log(data);
      setProspection(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  useEffect(() => {
    FetchProspection();
    const timer = setInterval(() => {
      FetchProspection();
    }, 10000);

    return () => clearInterval(timer);
  }, []);

  const getAuthHeaders = async () => {
    const {
      data: { session },
    } = await supabase.auth.getSession();
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session?.access_token}`,
      // "ngrok-skip-browser-warning": "true",
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // if (!intitule.trim()) return;
    // const headers = await getAuthHeaders();
    // const response = await fetch(
    //   "http://localhost:8000/backend/prospection/list",
    //   {
    //     method: "POST",
    //     headers,
    //     body: JSON.stringify({ intitule }),
    //   },
    // );

    setIsLoading(true);
    setStatusLogs([]);
    setActiveId("current");
    // const {
    //   data: { session },
    // } = await supabase.auth.getSession();

    // setStatusMessage("En cours...");

    try {
      const headers = await getAuthHeaders();
      const response = await fetch(
        "http://localhost:8000/backend/prospection/start_prospection",
        {
          method: "POST",
          headers,
          body: JSON.stringify({ intitule, details, mode, offre }),
        },
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      setStatusLogs([]);
      localStorage.removeItem("prospection_logs");
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        // const message = decoder.decode(value);
        // console.log("Message", message);
        // console.log("Morceau reçu :", message);
        console.log("Value brute du reader :", value);

        setStatusLogs((prev) => {
          const newLogs = [...prev, chunk];
          localStorage.setItem("prospection_logs", JSON.stringify(newLogs));
          return newLogs;
        });

        // setStatusMessage(message);
      }

      if (response.ok) {
        setIntitule("");
        FetchProspection();
      }
    } catch (error) {
      console.error("Erreur:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredProspection = prospection.filter((p) =>
    p.job_title?.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="min-h-screen bg-white p-4 md:p-6 font-sans">
      <div className="max-w-5xl mx-auto">
        <div className="mb-6">
          <h1 className="text-lg font-normal text-gray-900 tracking-tight">
            Prospection
          </h1>
          <p className="text-gray-500 text-xs mt-0.5">
            Gestion des prospections
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Formulaire compact */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded border border-gray-200 p-4">
              <h2 className="text-sm font-normal text-gray-900 mb-4">
                Nouvelle prospection
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  {/* <label
                    htmlFor="intitule"
                    className="block text-xs font-normal text-gray-600 mb-1.5"
                  >
                    Intitulé du métier
                  </label>
                  <input
                    id="intitule"
                    type="text"
                    value={intitule}
                    onChange={(e) => setIntitule(e.target.value)}
                    disabled={isLoading}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                    placeholder="Ex: Développeur Front-end"
                    required
                  />
                  <label
                    htmlFor="intitule"
                    className="block text-xs font-normal text-gray-600 mb-1.5"
                  >
                    Donner des détails pour les messages privés généré par le
                    model
                  </label>
                  <input
                    id="Details_message"
                    type="text"
                    value={intitule}
                    onChange={(e) => setIntitule(e.target.value)}
                    disabled={isLoading}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                    placeholder="Détails"
                    required
                  />
                  <label
                    htmlFor="type_of_prospect"
                    className="block text-xs font-normal text-gray-600 mb-1.5"
                  >
                    Type de prospection
                  </label>
                  <input
                    id="type_prospection"
                    type="radio"
                    // value={type_prospection}
                    // onChange={(e) => setIntitule(e.target.value)}
                    disabled={isLoading}
                    // className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                    required
                  />*/}
                  <div className="space-y-4">
                    {/* Input Métier */}
                    <div>
                      <label
                        htmlFor="intitule"
                        className="block text-xs font-normal text-gray-600 mb-1.5"
                      >
                        Intitulé du métier
                      </label>
                      <input
                        id="intitule"
                        type="text"
                        value={intitule}
                        onChange={(e) => setIntitule(e.target.value)}
                        disabled={isLoading}
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                        placeholder="Ex: Développeur Front-end"
                        // required
                      />
                    </div>

                    {/* Input Détails */}
                    <div>
                      <label
                        htmlFor="details"
                        className="block text-xs font-normal text-gray-600 mb-1.5"
                      >
                        Détails pour les messages privés (IA)
                      </label>
                      <input
                        id="details"
                        type="text"
                        value={details}
                        onChange={(e) => setDetails(e.target.value)}
                        disabled={isLoading}
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                        placeholder="Ex: Mentionner l'offre..."
                        // required
                      />
                    </div>

                    <div>
                      <label
                        htmlFor="offre"
                        className="block text-xs font-normal text-gray-600 mb-1.5"
                      >
                        Uploader l'offre pour facilier la recherche
                      </label>
                      <input
                        id="offre"
                        type="file"
                        onchange={(e) => setOffre(e.target.files[0])}
                        // value={offre}
                        disabled={isLoading}
                        accept=".pdf, .doc, .docx"
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50" // required
                      />
                    </div>

                    {/* Radio Buttons Type */}
                    <div>
                      <label className="block text-xs font-normal text-gray-600 mb-2">
                        Type de prospection
                      </label>
                      <div className="flex gap-4">
                        <label className="flex items-center text-xs font-normal text-gray-700 cursor-pointer">
                          <input
                            type="radio"
                            name="type_prospection"
                            value="prospection"
                            checked={mode === "prospection"}
                            onChange={(e) => setMode(e.target.value)}
                            disabled={isLoading}
                            className="mr-2 accent-black"
                          />
                          Prospection
                        </label>
                        <label className="flex items-center text-xs font-normal text-gray-700 cursor-pointer">
                          <input
                            type="radio"
                            name="type_prospection"
                            value="demarchage"
                            checked={mode === "demarchage"}
                            onChange={(e) => setMode(e.target.value)}
                            disabled={isLoading}
                            className="mr-2 accent-black"
                          />
                          Démarchage
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
                <button
                  type="submit"
                  disabled={isLoading || !intitule.trim()}
                  className={`w-full py-2 text-xs rounded transition-colors
                    ${
                      isLoading || !intitule.trim()
                        ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                        : "bg-black hover:bg-gray-800 text-white"
                    }`}
                >
                  {isLoading ? (
                    <span className="flex items-center justify-center">
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                      Traitement...
                    </span>
                  ) : (
                    "Lancer la prospection"
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Liste sobre */}
          <div className="lg:col-span-2">
            <div className="bg-white border border-gray-200 rounded">
              {/* En-tête minimal */}
              <div className="p-4 border-b border-gray-100">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h2 className="text-sm font-normal text-gray-900">
                      Historique
                    </h2>
                    <p className="text-gray-500 text-xs mt-0.5">
                      {prospection.length} prospection
                      {prospection.length !== 1 ? "s" : ""}
                    </p>
                  </div>
                  <div className="relative">
                    <input
                      type="text"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full sm:w-48 px-3 py-1.5 text-xs bg-white border border-gray-300 rounded shadow-none outline-none"
                      placeholder="Rechercher..."
                    />

                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </div>
                </div>
              </div>

              {/* Liste compacte */}
              <div className="divide-y divide-gray-100 max-h-[500px] overflow-y-auto">
                {filteredProspection.length === 0 ? (
                  <div className="p-6 text-center">
                    <svg
                      className="w-8 h-8 text-gray-300 mx-auto mb-3"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                    <p className="text-gray-400 text-xs">
                      {searchTerm ? "Aucun résultat" : "Aucune prospection"}
                    </p>
                  </div>
                ) : (
                  filteredProspection.map((p) => (
                    <div
                      key={p.id}
                      // className={`p-3 hover:bg-gray-50 transition-colors ${
                      //   expandedProspection === p.id ? "bg-gray-50" : ""
                      // }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1.5">
                            <h3 className="text-xs font-normal text-gray-900 truncate">
                              {p.job_title}
                            </h3>

                            {p.is_active && (
                              <div className="flex items-center text-blue-600">
                                <div className="animate-spin rounded-full h-3 w-3 border-2 border-current border-t-transparent"></div>
                              </div>
                            )}
                          </div>
                          {p.is_active && statusLogs.length > 0 && (
                            <div className="mb-3 p-2 bg-gray-50 border border-gray-100 rounded text-[10px] font-mono max-h-32 overflow-y-auto">
                              {statusLogs.map((log, index) => (
                                <div
                                  key={index}
                                  className="text-blue-600 border-l-2 border-blue-200 pl-2 mb-0.5"
                                >
                                  {log}
                                </div>
                              ))}
                            </div>
                          )}
                          {/* {statusLogs.length > 0 && (
                            <div className="mt-4 p-3 bg-gray-50 border border-gray-200 rounded text-[10px] font-mono max-h-40 overflow-y-auto">
                              <p className="text-gray-400 mb-1">
                                Logs en direct :
                              </p>
                              {statusLogs.map((log, index) => (
                                <div
                                  key={index}
                                  className="text-blue-600 border-l-2 border-blue-200 pl-2 mb-1"
                                >
                                  {log}
                                </div>
                              ))}
                            </div>
                          )}*/}

                          <div className="flex items-center text-gray-400 text-[10px] gap-3">
                            <span className="flex items-center">
                              <svg
                                className="w-2.5 h-2.5 mr-1"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                                />
                              </svg>
                              {new Date(p.created_at).toLocaleDateString(
                                "fr-FR",
                                {
                                  day: "numeric",
                                  month: "short",
                                  year: "numeric",
                                },
                              )}
                            </span>
                            <span className="flex items-center">
                              <svg
                                className="w-2.5 h-2.5 mr-1"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                />
                              </svg>
                              {new Date(p.created_at).toLocaleTimeString(
                                "fr-FR",
                                {
                                  hour: "2-digit",
                                  minute: "2-digit",
                                },
                              )}
                            </span>
                            {p.hour_start && (
                              <span className="flex items-center text-indigo-600 font-semibold bg-indigo-50 px-1.5 py-0.5 rounded">
                                <svg
                                  className="w-2.5 h-2.5 mr-1"
                                  fill="currentColor"
                                  viewBox="0 0 20 20"
                                >
                                  <path
                                    fillRule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                                    clipRule="evenodd"
                                  />
                                </svg>
                                Lancement automatique demain à :{" "}
                                {p.hour_start.split("T")[1].slice(0, 5)}
                              </span>
                            )}
                          </div>
                        </div>

                        <button
                          onClick={() => setItemToDelete(p.id)}
                          className="text-gray-300 hover:text-red-500 p-1 transition-colors ml-2"
                        >
                          <svg
                            className="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      {itemToDelete && (
        <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white border border-gray-200 rounded-lg p-6 max-w-sm w-full shadow-xl">
            <h3 className="text-sm font-medium text-gray-900">
              Supprimer la prospection ?
            </h3>
            <p className="text-xs text-gray-500 mt-2">
              La suppression est définitive
            </p>
            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => setItemToDelete(null)}
                className="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded"
              >
                Annuler
              </button>
              <button
                onClick={async () => {
                  await supabase
                    .from("prospection_settings")
                    .delete()
                    .eq("id", itemToDelete);
                  setItemToDelete(null);
                  FetchProspection();
                }}
                className="px-3 py-1.5 text-xs bg-red-600 text-white hover:bg-red-700 rounded"
              >
                Confirmer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Prospection;
