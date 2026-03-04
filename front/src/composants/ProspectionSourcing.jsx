import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";
function ProspectionSourcing() {
  const [intitule, setIntitule] = useState("");

  const [segment, setSegment] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [prospection, setProspection] = useState([]);
  const [itemToDelete, setItemToDelete] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeId, setActiveId] = useState(null);
  const [mode, setMode] = useState("");
  const [details, setDetails] = useState("");
  const [candidatrecherche, setcandidatrecherche] = useState("");
  const [post, setPost] = useState("");
  const [statusLogs, setStatusLogs] = useState(() => {
    const saved = localStorage.getItem("prospection_logs");
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    const activeProspection = prospection.find((p) => p.is_active === true);
    if (prospection.length > 0 && !activeProspection) {
      setStatusLogs([]);
      localStorage.removeItem("prospection_logs");
    }
  }, [prospection]);

  const FetchProspection = async () => {
    try {
      const headers = await getAuthHeaders();
      const res = await fetch(
        "http://192.168.10.112:8003/backend/prospection/list",
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
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setIsLoading(true);
    setStatusLogs([]);
    setActiveId("current");

    try {
      const headers = await getAuthHeaders();
      const response = await fetch(
        "http://192.168.10.112:8003/backend/prospection/start_prospection",
        {
          method: "POST",
          headers,
          body: JSON.stringify({
            intitule,
            details,
            mode,
            candidatrecherche,
            post,
            segment,
            telephone: "",
            full_name: "",
          }),
        },
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      setStatusLogs([]);
      localStorage.removeItem("prospection_logs");
      while (true) {
        try {
          const { value, done } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value);

          console.log("Value brute du reader :", value);

          setStatusLogs((prev) => {
            try {
              const newLogs = [...prev, chunk];
              localStorage.setItem("prospection_logs", JSON.stringify(newLogs));
              return newLogs;
            } catch (storageError) {
              console.error("Erreur LocalStorage (saturé ?):", storageError);
              return [...prev, chunk];
            }
          });
        } catch (streamError) {
          console.error("bug dans la lecture du stream :", streamError);
          break;
        }
      }

      if (response.ok) {
        setIntitule("");
        setDetails("");
        setSegment("");
        setcandidatrecherche("");
        setPost("");
        setMode("");
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
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-normal text-gray-900 tracking-tight">
              Prospection et sourcing
            </h1>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="#0077B5"
            >
              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.238 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
            </svg>
          </div>
          <p className="text-gray-500 text-xs mt-0.5">Gestion</p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Formulaire compact */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded border border-gray-200 p-4">
              <h6>Nouveau lancement</h6>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-x-6 gap-y-2 mt-2 w-fit">
                  {["Entreprises", "Offres", "Annonces", "Personnes"].map(
                    (val) => (
                      <label
                        key={val}
                        className="flex items-center gap-2 text-[11px] text-gray-600 cursor-pointer hover:text-blue-600"
                      >
                        <input
                          type="radio"
                          name="filtre"
                          value={val}
                          className="w-3 h-3 accent-blue-600"
                          onChange={(e) => setSegment(e.target.value)}
                          disabled={isLoading}
                        />
                        {val}
                      </label>
                    ),
                  )}
                </div>
                <div>
                  <div className="space-y-4">
                    <div>
                      <label
                        htmlFor="post"
                        className="block text-xs font-normal text-gray-600 mb-1.5"
                      >
                        Indication au modèle concernant les posts
                      </label>
                      <input
                        id="post"
                        type="text"
                        value={post}
                        onChange={(e) => setPost(e.target.value)}
                        disabled={isLoading}
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                        placeholder="Ex: Soi court et précis"
                        // required
                      />
                    </div>
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
                    {/* </div>
                    )}*/}

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

                    {/* Radio Buttons Type */}
                    <div>
                      <label className="block text-xs font-normal text-gray-600 mb-2">
                        Type de lancement
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
                            required
                          />
                          Prospection
                        </label>
                        <label className="flex items-center text-xs font-normal text-gray-700 cursor-pointer">
                          <input
                            type="radio"
                            name="type_prospection"
                            value="sourcing"
                            checked={mode === "sourcing"}
                            onChange={(e) => setMode(e.target.value)}
                            disabled={isLoading}
                            className="mr-2 accent-black"
                            required
                          />
                          Sourcing
                        </label>
                      </div>
                    </div>
                    {mode === "sourcing" && (
                      <div>
                        <div className="space-y-4">
                          <div>
                            <label
                              htmlFor="post"
                              className="block text-xs font-normal text-gray-600 mb-1.5"
                            >
                              Indiquer directement le profil recherché
                            </label>
                            <input
                              id="post"
                              type="text"
                              value={candidatrecherche}
                              onChange={(e) =>
                                setcandidatrecherche(e.target.value)
                              }
                              disabled={isLoading}
                              className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                              placeholder="Ex: On recherche un candidat situé..."
                              // required
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <button
                  type="submit"
                  disabled={
                    isLoading ||
                    !intitule.trim() ||
                    prospection.some((p) => p.is_active)
                  }
                  className={`w-full py-2 text-xs rounded transition-colors
                    ${
                      isLoading ||
                      !intitule.trim() ||
                      prospection.some((p) => p.is_active)
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
                    "Lancer"
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
                    <h1></h1>
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
                    <div key={p.id}>
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

                          <div className="flex flex-wrap items-center gap-2">
                            <div className="flex items-center gap-1.5 px-2 py-1 bg-gray-100 rounded-md text-gray-700 text-xs">
                              <svg
                                className="w-3.5 h-3.5 text-gray-500"
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
                              <span>
                                {new Date(p.created_at).toLocaleDateString(
                                  "fr-FR",
                                  {
                                    day: "numeric",
                                    month: "short",
                                    year: "numeric",
                                  },
                                )}
                              </span>
                              <span className="text-gray-400 mx-0.5">à</span>
                              <span className="font-medium">
                                {new Date(p.created_at).toLocaleTimeString(
                                  "fr-FR",
                                  {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                  },
                                )}
                              </span>
                            </div>

                            {p.hour_start && (
                              <div className="flex items-center gap-1.5 px-2 py-1 bg-gradient-to-r from-indigo-50 to-purple-50 text-indigo-700 rounded-md text-xs border border-indigo-100">
                                <svg
                                  className="w-3.5 h-3.5"
                                  fill="currentColor"
                                  viewBox="0 0 20 20"
                                >
                                  <path d="M11.3 3.046l1.396-1.408a.75.75 0 011.06 0l1.408 1.408a.75.75 0 010 1.06l-1.408 1.408a.75.75 0 01-1.06 0L11.3 4.106a.75.75 0 010-1.06zM15.956 7.75l-1.408-1.408a.75.75 0 00-1.06 0L12.08 7.75a.75.75 0 000 1.06l1.408 1.408a.75.75 0 001.06 0l1.408-1.408a.75.75 0 000-1.06zM6.02 4.106a.75.75 0 010 1.06L4.61 6.575a.75.75 0 01-1.06 0L2.142 5.166a.75.75 0 010-1.06L3.55 2.698a.75.75 0 011.06 0l1.409 1.408zM8.25 10.5a.75.75 0 00-.75.75v4.5a.75.75 0 001.5 0v-4.5a.75.75 0 00-.75-.75z" />
                                </svg>
                                <span>
                                  Auto • demain{" "}
                                  {p.hour_start.split("T")[1].slice(0, 5)}
                                </span>
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="text-[10px] text-gray-500 mt-1">
                          {p.total_connexions ?? 0} demandes de connexions
                          envoyés · {p.total_messages ?? 0} personnes contactés
                          par messages
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
            <h3 className="text-sm font-medium text-gray-900">Supprimer ?</h3>
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

export default ProspectionSourcing;
