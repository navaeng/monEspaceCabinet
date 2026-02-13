import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";
import mammoth from "mammoth";

function ProspectionSourcing() {
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
  const [post, setPost] = useState("");
  const [statusLogs, setStatusLogs] = useState(() => {
    const saved = localStorage.getItem("prospection_logs");
    return saved ? JSON.parse(saved) : [];
  });

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    const isDocx = file.name.endsWith(".docx");

    reader.onload = async (event) => {
      try {
        if (isDocx) {
          const { value } = await mammoth.extractRawText({
            arrayBuffer: event.target.result,
          });
          setOffre(value);
        } else {
          setOffre(event.target.result);
        }
      } catch (error) {
        console.error("Error processing file:", error);
      }
    };
    file.name.endsWith("docx")
      ? reader.readAsArrayBuffer(file)
      : reader.readAsText(file);
  };

  // const [statusLogs, setStatusLogs] = useState(() => {
  //   const saved = localStorage.getItem("prospection_logs");
  //   return saved ? JSON.parse(saved) : [];
  // });

  useEffect(() => {
    const activeProspection = prospection.find((p) => p.is_active === true);
    if (prospection.length > 0 && !activeProspection) {
      setStatusLogs([]);
      localStorage.removeItem("prospection_logs");
    }
  }, [prospection]); // ceci pour raffraichir a chaque fois que la liste change

  const FetchProspection = async () => {
    try {
      const headers = await getAuthHeaders();
      const res = await fetch(
        "http://localhost:8003/backend/prospection/list",
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
        "http://localhost:8003/backend/linkedin/start_chrome",
        {
          method: "POST",
          headers,
          body: JSON.stringify({
            intitule,
            details,
            mode,
            offre,
            post,
            telephone: "",
            full_name: "",
          }),
        },
      );

      // const response = await fetch(
      //   "http://192.168.122.1:8000/backend/prospection/start_chrome",
      //   {
      //     method: "POST",
      //     headers,
      //     body: JSON.stringify({ intitule, details, mode, offre }),
      //   },
      // );

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
            Prospection et sourcing
          </h1>
          <p className="text-gray-500 text-xs mt-0.5">Gestion</p>
        </div>

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
            placeholder="post..."
            // required
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Formulaire compact */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded border border-gray-200 p-4">
              <h2 className="text-sm font-normal text-gray-900 mb-4">
                Nouveau lancement
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
                    {/* <div>
                      <label className="block text-xs font-normal text-gray-600 mb-2">
                        Type d'analyse
                      </label>
                      <div className="flex gap-4">
                        <label className="flex items-center text-xs font-normal text-gray-700 cursor-pointer">
                          <input
                            type="radio"
                            name="people_selection"
                            value="people_precise"
                            checked={people === "people_precise"}
                            onChange={(e) => Setpeople_precise(e.target.value)}
                            disabled={isLoading}
                            className="mr-2 accent-black"
                          />
                          Recherche inteligente
                        </label>
                        <label className="flex items-center text-xs font-normal text-gray-700 cursor-pointer">
                          <input
                            type="radio"
                            name="people_selection"
                            value="people_not_precise"
                            checked={people === "people_not_precise"}
                            onChange={(e) => Setpeople_precise(e.target.value)}
                            disabled={isLoading}
                            className="mr-2 accent-black"
                          />
                          Contacter du monde
                        </label>
                      </div>
                    </div>*/}

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
                        <label
                          htmlFor="offre"
                          className="block text-xs font-normal text-gray-600 mb-1.5"
                        >
                          Uploader l'offre pour facilier la recherche
                        </label>
                        <input
                          id="offre"
                          type="file"
                          onChange={handleFileChange}
                          disabled={isLoading}
                          accept=".pdf, .doc, .docx"
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50" // required
                        />
                      </div>
                    )}
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
                    "Lancer"
                  )}
                </button>
                <p className="text-gray-500 text-xs mt-0.5">
                  N'actualisez pas la page au lancement
                </p>
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
                    {/* {statusLogs.length > 0 && (
                      <div className="mt-4 p-3 bg-gray-50 border border-gray-200 rounded text-[10px] font-mono max-h-40 overflow-y-auto">
                        <p className="text-gray-400 mb-1">Logs en direct :</p>
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

// import { useState, useEffect } from "react";
// import { supabase } from "../supabaseClient";
// import mammoth from "mammoth";

// function ProspectionSourcing() {
//   // État principal
//   const [formData, setFormData] = useState({
//     intitule: "",
//     details: "",
//     mode: "",
//     people: "",
//     offre: "",
//   });

//   const [isLoading, setIsLoading] = useState(false);
//   const [prospection, setProspection] = useState([]);
//   const [searchTerm, setSearchTerm] = useState("");
//   const [itemToDelete, setItemToDelete] = useState(null);
//   const [statusLogs, setStatusLogs] = useState(() => {
//     const saved = localStorage.getItem("prospection_logs");
//     return saved ? JSON.parse(saved) : [];
//   });

//   // Gestion des champs du formulaire
//   const handleInputChange = (field, value) => {
//     setFormData((prev) => ({ ...prev, [field]: value }));
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (!file) return;

//     const reader = new FileReader();
//     const isDocx = file.name.endsWith(".docx");

//     reader.onload = async (event) => {
//       try {
//         if (isDocx) {
//           const { value } = await mammoth.extractRawText({
//             arrayBuffer: event.target.result,
//           });
//           handleInputChange("offre", value);
//         } else {
//           handleInputChange("offre", event.target.result);
//         }
//       } catch (error) {
//         console.error("Error processing file:", error);
//       }
//     };

//     file.name.endsWith("docx")
//       ? reader.readAsArrayBuffer(file)
//       : reader.readAsText(file);
//   };

//   // Nettoyage des logs lorsque pas de prospection active
//   useEffect(() => {
//     const activeProspection = prospection.find((p) => p.is_active === true);
//     if (prospection.length > 0 && !activeProspection) {
//       setStatusLogs([]);
//       localStorage.removeItem("prospection_logs");
//     }
//   }, [prospection]);

//   // Récupération des prospections
//   const fetchProspection = async () => {
//     try {
//       const headers = await getAuthHeaders();
//       const res = await fetch(
//         "http://localhost:8000/backend/prospection/list",
//         {
//           method: "GET",
//           headers,
//         },
//       );
//       const data = await res.json();
//       setProspection(Array.isArray(data) ? data : []);
//     } catch (error) {
//       console.error("Erreur:", error);
//     }
//   };

//   useEffect(() => {
//     fetchProspection();
//     const timer = setInterval(() => {
//       fetchProspection();
//     }, 10000);

//     return () => clearInterval(timer);
//   }, []);

//   const getAuthHeaders = async () => {
//     const {
//       data: { session },
//     } = await supabase.auth.getSession();
//     return {
//       "Content-Type": "application/json",
//       Authorization: `Bearer ${session?.access_token}`,
//     };
//   };

//   // Soumission du formulaire
//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!formData.intitule.trim()) return;

//     setIsLoading(true);
//     setStatusLogs([]);

//     try {
//       const headers = await getAuthHeaders();
//       const response = await fetch(
//         "http://localhost:8000/backend/prospection/start_prospection",
//         {
//           method: "POST",
//           headers,
//           body: JSON.stringify(formData),
//         },
//       );

//       const reader = response.body.getReader();
//       const decoder = new TextDecoder();

//       setStatusLogs([]);
//       localStorage.removeItem("prospection_logs");

//       while (true) {
//         const { value, done } = await reader.read();
//         if (done) break;

//         const chunk = decoder.decode(value);
//         setStatusLogs((prev) => {
//           const newLogs = [...prev, chunk];
//           localStorage.setItem("prospection_logs", JSON.stringify(newLogs));
//           return newLogs;
//         });
//       }

//       if (response.ok) {
//         setFormData({
//           intitule: "",
//           details: "",
//           mode: "",
//           people: "",
//           offre: "",
//         });
//         fetchProspection();
//       }
//     } catch (error) {
//       console.error("Erreur:", error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Filtrage
//   const filteredProspection = prospection.filter((p) =>
//     p.job_title?.toLowerCase().includes(searchTerm.toLowerCase()),
//   );

//   // Composants réutilisables
//   const FormSection = ({ title, children }) => (
//     <div className="mb-6">
//       <h3 className="text-xs font-semibold text-gray-700 mb-3 uppercase tracking-wider">
//         {title}
//       </h3>
//       {children}
//     </div>
//   );

//   const InputField = ({
//     label,
//     id,
//     type = "text",
//     value,
//     onChange,
//     placeholder,
//     disabled,
//     required = false,
//   }) => (
//     <div className="mb-4">
//       <label
//         htmlFor={id}
//         className="block text-xs font-medium text-gray-600 mb-1.5"
//       >
//         {label}
//       </label>
//       <input
//         id={id}
//         type={type}
//         value={value}
//         onChange={onChange}
//         disabled={disabled}
//         placeholder={placeholder}
//         required={required}
//         className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent transition-all disabled:bg-gray-50 disabled:cursor-not-allowed"
//       />
//     </div>
//   );

//   const RadioGroup = ({ label, name, options, value, onChange, disabled }) => (
//     <div className="mb-4">
//       <label className="block text-xs font-medium text-gray-600 mb-2">
//         {label}
//       </label>
//       <div className="flex gap-4">
//         {options.map((option) => (
//           <label
//             key={option.value}
//             className="flex items-center text-sm text-gray-700 cursor-pointer"
//           >
//             <input
//               type="radio"
//               name={name}
//               value={option.value}
//               checked={value === option.value}
//               onChange={onChange}
//               disabled={disabled}
//               className="mr-2 w-4 h-4 text-black border-gray-300 focus:ring-black"
//             />
//             {option.label}
//           </label>
//         ))}
//       </div>
//     </div>
//   );

//   return (
//     <div className="min-h-screen bg-gray-50 p-6 font-sans">
//       <div className="max-w-7xl mx-auto">
//         {/* En-tête */}
//         <div className="mb-8">
//           <h1 className="text-2xl font-semibold text-gray-900">
//             Prospection & Sourcing
//           </h1>
//           <p className="text-gray-500 text-sm mt-1">
//             Gérez vos campagnes de recrutement automatisées
//           </p>
//         </div>

//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
//           {/* Colonne gauche - Formulaire */}
//           <div className="lg:col-span-1">
//             <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-6">
//               <div className="flex items-center justify-between mb-6">
//                 <h2 className="text-lg font-semibold text-gray-900">
//                   Nouvelle campagne
//                 </h2>
//                 <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">
//                   {isLoading ? "En cours..." : "Prêt"}
//                 </span>
//               </div>

//               <form onSubmit={handleSubmit} className="space-y-6">
//                 <FormSection title="Description du poste">
//                   <InputField
//                     label="Intitulé du métier *"
//                     id="intitule"
//                     value={formData.intitule}
//                     onChange={(e) =>
//                       handleInputChange("intitule", e.target.value)
//                     }
//                     placeholder="Ex: Développeur Front-end React"
//                     disabled={isLoading}
//                     required
//                   />

//                   <InputField
//                     label="Détails pour personnalisation IA"
//                     id="details"
//                     value={formData.details}
//                     onChange={(e) =>
//                       handleInputChange("details", e.target.value)
//                     }
//                     placeholder="Informations spécifiques pour les messages..."
//                     disabled={isLoading}
//                   />
//                 </FormSection>

//                 <FormSection title="Stratégie de recherche">
//                   <RadioGroup
//                     label="Type d'analyse"
//                     name="people"
//                     options={[
//                       {
//                         value: "people_precise",
//                         label: "Recherche intelligente",
//                       },
//                       {
//                         value: "people_not_precise",
//                         label: "Contacter du monde",
//                       },
//                     ]}
//                     value={formData.people}
//                     onChange={(e) =>
//                       handleInputChange("people", e.target.value)
//                     }
//                     disabled={isLoading}
//                   />

//                   <RadioGroup
//                     label="Mode de lancement"
//                     name="mode"
//                     options={[
//                       { value: "prospection", label: "Prospection" },
//                       { value: "sourcing", label: "Sourcing" },
//                     ]}
//                     value={formData.mode}
//                     onChange={(e) => handleInputChange("mode", e.target.value)}
//                     disabled={isLoading}
//                   />
//                 </FormSection>

//                 {formData.mode === "sourcing" && (
//                   <FormSection title="Offre d'emploi">
//                     <div className="mb-4">
//                       <label className="block text-xs font-medium text-gray-600 mb-1.5">
//                         Fichier de l'offre
//                       </label>
//                       <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-gray-400 transition-colors">
//                         <input
//                           type="file"
//                           onChange={handleFileChange}
//                           disabled={isLoading}
//                           accept=".pdf, .doc, .docx"
//                           className="hidden"
//                           id="file-upload"
//                         />
//                         <label
//                           htmlFor="file-upload"
//                           className="cursor-pointer block"
//                         >
//                           <svg
//                             className="w-8 h-8 text-gray-400 mx-auto mb-2"
//                             fill="none"
//                             stroke="currentColor"
//                             viewBox="0 0 24 24"
//                           >
//                             <path
//                               strokeLinecap="round"
//                               strokeLinejoin="round"
//                               strokeWidth={1.5}
//                               d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
//                             />
//                           </svg>
//                           <span className="text-sm text-gray-600">
//                             Glissez-déposez ou cliquez pour uploader
//                           </span>
//                           <p className="text-xs text-gray-400 mt-1">
//                             PDF, DOC, DOCX (max. 10MB)
//                           </p>
//                         </label>
//                       </div>
//                     </div>
//                   </FormSection>
//                 )}

//                 <button
//                   type="submit"
//                   disabled={isLoading || !formData.intitule.trim()}
//                   className={`
//                     w-full py-3 px-4 rounded-lg font-medium transition-all duration-200
//                     ${
//                       isLoading || !formData.intitule.trim()
//                         ? "bg-gray-100 text-gray-400 cursor-not-allowed"
//                         : "bg-gray-900 text-white hover:bg-gray-800 active:scale-[0.98]"
//                     }
//                   `}
//                 >
//                   {isLoading ? (
//                     <span className="flex items-center justify-center">
//                       <svg
//                         className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
//                         xmlns="http://www.w3.org/2000/svg"
//                         fill="none"
//                         viewBox="0 0 24 24"
//                       >
//                         <circle
//                           className="opacity-25"
//                           cx="12"
//                           cy="12"
//                           r="10"
//                           stroke="currentColor"
//                           strokeWidth="4"
//                         ></circle>
//                         <path
//                           className="opacity-75"
//                           fill="currentColor"
//                           d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
//                         ></path>
//                       </svg>
//                       Lancement en cours...
//                     </span>
//                   ) : (
//                     "Lancer la campagne"
//                   )}
//                 </button>

//                 <div className="text-xs text-gray-500 p-3 bg-blue-50 rounded-lg border border-blue-100">
//                   <svg
//                     className="w-4 h-4 inline-block mr-1 mb-0.5"
//                     fill="none"
//                     stroke="currentColor"
//                     viewBox="0 0 24 24"
//                   >
//                     <path
//                       strokeLinecap="round"
//                       strokeLinejoin="round"
//                       strokeWidth={2}
//                       d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
//                     />
//                   </svg>
//                   Ne quittez pas cette page pendant le lancement. Les résultats
//                   s'afficheront automatiquement.
//                 </div>
//               </form>
//             </div>
//           </div>

//           {/* Colonne droite - Historique */}
//           <div className="lg:col-span-2">
//             <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
//               {/* En-tête avec recherche et stats */}
//               <div className="p-6 border-b border-gray-100">
//                 <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
//                   <div>
//                     <h2 className="text-lg font-semibold text-gray-900">
//                       Historique des campagnes
//                     </h2>
//                     <div className="flex items-center gap-3 mt-1">
//                       <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">
//                         {prospection.length} campagne
//                         {prospection.length !== 1 ? "s" : ""}
//                       </span>
//                       {prospection.some((p) => p.is_active) && (
//                         <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-600 rounded-full flex items-center">
//                           <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse mr-1.5"></div>
//                           En cours
//                         </span>
//                       )}
//                     </div>
//                   </div>

//                   <div className="relative">
//                     <div className="relative">
//                       <svg
//                         className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
//                         fill="none"
//                         stroke="currentColor"
//                         viewBox="0 0 24 24"
//                       >
//                         <path
//                           strokeLinecap="round"
//                           strokeLinejoin="round"
//                           strokeWidth={2}
//                           d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
//                         />
//                       </svg>
//                       <input
//                         type="text"
//                         value={searchTerm}
//                         onChange={(e) => setSearchTerm(e.target.value)}
//                         className="pl-10 pr-4 py-2 w-full sm:w-64 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent"
//                         placeholder="Rechercher une campagne..."
//                       />
//                     </div>
//                   </div>
//                 </div>
//               </div>

//               {/* Liste des campagnes */}
//               <div className="divide-y divide-gray-100 max-h-[600px] overflow-y-auto">
//                 {filteredProspection.length === 0 ? (
//                   <div className="p-12 text-center">
//                     <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
//                       <svg
//                         className="w-8 h-8 text-gray-400"
//                         fill="none"
//                         stroke="currentColor"
//                         viewBox="0 0 24 24"
//                       >
//                         <path
//                           strokeLinecap="round"
//                           strokeLinejoin="round"
//                           strokeWidth={1.5}
//                           d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
//                         />
//                       </svg>
//                     </div>
//                     <h3 className="text-gray-700 font-medium mb-1">
//                       {searchTerm
//                         ? "Aucune campagne trouvée"
//                         : "Aucune campagne"}
//                     </h3>
//                     <p className="text-gray-500 text-sm">
//                       {searchTerm
//                         ? "Essayez avec d'autres termes"
//                         : "Lancez votre première campagne"}
//                     </p>
//                   </div>
//                 ) : (
//                   filteredProspection.map((p) => (
//                     <div
//                       key={p.id}
//                       className="p-5 hover:bg-gray-50 transition-colors"
//                     >
//                       <div className="flex items-start justify-between">
//                         <div className="flex-1 min-w-0">
//                           <div className="flex items-center gap-3 mb-3">
//                             <h3 className="text-base font-medium text-gray-900 truncate">
//                               {p.job_title}
//                             </h3>

//                             {/* Badges d'état */}
//                             <div className="flex items-center gap-2">
//                               {p.is_active && (
//                                 <span className="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-600 rounded-full flex items-center">
//                                   <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse mr-1.5"></div>
//                                   En cours
//                                 </span>
//                               )}

//                               {p.hour_start && (
//                                 <span className="px-2 py-0.5 text-xs font-medium bg-indigo-100 text-indigo-600 rounded-full flex items-center">
//                                   <svg
//                                     className="w-3 h-3 mr-1"
//                                     fill="currentColor"
//                                     viewBox="0 0 20 20"
//                                   >
//                                     <path
//                                       fillRule="evenodd"
//                                       d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
//                                       clipRule="evenodd"
//                                     />
//                                   </svg>
//                                   Auto: {p.hour_start.split("T")[1].slice(0, 5)}
//                                 </span>
//                               )}
//                             </div>
//                           </div>

//                           {/* Logs en temps réel si actif */}
//                           {p.is_active && statusLogs.length > 0 && (
//                             <div className="mb-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
//                               <div className="flex items-center justify-between mb-2">
//                                 <span className="text-xs font-medium text-gray-600">
//                                   Logs en direct
//                                 </span>
//                                 <span className="text-xs text-gray-400">
//                                   {statusLogs.length} message
//                                   {statusLogs.length !== 1 ? "s" : ""}
//                                 </span>
//                               </div>
//                               <div className="text-xs font-mono space-y-1 max-h-32 overflow-y-auto">
//                                 {statusLogs.map((log, index) => (
//                                   <div
//                                     key={index}
//                                     className="text-blue-600 border-l-2 border-blue-300 pl-2 py-0.5"
//                                   >
//                                     {log}
//                                   </div>
//                                 ))}
//                               </div>
//                             </div>
//                           )}

//                           {/* Métadonnées */}
//                           <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
//                             <span className="flex items-center">
//                               <svg
//                                 className="w-4 h-4 mr-1.5"
//                                 fill="none"
//                                 stroke="currentColor"
//                                 viewBox="0 0 24 24"
//                               >
//                                 <path
//                                   strokeLinecap="round"
//                                   strokeLinejoin="round"
//                                   strokeWidth={1.5}
//                                   d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
//                                 />
//                               </svg>
//                               {new Date(p.created_at).toLocaleDateString(
//                                 "fr-FR",
//                                 {
//                                   day: "numeric",
//                                   month: "short",
//                                   year: "numeric",
//                                 },
//                               )}
//                             </span>

//                             <span className="flex items-center">
//                               <svg
//                                 className="w-4 h-4 mr-1.5"
//                                 fill="none"
//                                 stroke="currentColor"
//                                 viewBox="0 0 24 24"
//                               >
//                                 <path
//                                   strokeLinecap="round"
//                                   strokeLinejoin="round"
//                                   strokeWidth={1.5}
//                                   d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
//                                 />
//                               </svg>
//                               {new Date(p.created_at).toLocaleTimeString(
//                                 "fr-FR",
//                                 {
//                                   hour: "2-digit",
//                                   minute: "2-digit",
//                                 },
//                               )}
//                             </span>
//                           </div>
//                         </div>

//                         {/* Bouton suppression */}
//                         <button
//                           onClick={() => setItemToDelete(p.id)}
//                           className="ml-4 p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
//                           title="Supprimer"
//                         >
//                           <svg
//                             className="w-4 h-4"
//                             fill="none"
//                             stroke="currentColor"
//                             viewBox="0 0 24 24"
//                           >
//                             <path
//                               strokeLinecap="round"
//                               strokeLinejoin="round"
//                               strokeWidth={1.5}
//                               d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
//                             />
//                           </svg>
//                         </button>
//                       </div>
//                     </div>
//                   ))
//                 )}
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Modal de confirmation de suppression */}
//       {itemToDelete && (
//         <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
//           <div className="bg-white rounded-2xl shadow-2xl p-6 max-w-md w-full">
//             <div className="flex items-center gap-3 mb-4">
//               <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
//                 <svg
//                   className="w-5 h-5 text-red-600"
//                   fill="none"
//                   stroke="currentColor"
//                   viewBox="0 0 24 24"
//                 >
//                   <path
//                     strokeLinecap="round"
//                     strokeLinejoin="round"
//                     strokeWidth={2}
//                     d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.998-.833-2.732 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z"
//                   />
//                 </svg>
//               </div>
//               <div>
//                 <h3 className="font-semibold text-gray-900">
//                   Supprimer la campagne
//                 </h3>
//                 <p className="text-sm text-gray-500">
//                   Cette action est irréversible
//                 </p>
//               </div>
//             </div>

//             <div className="flex justify-end gap-3 mt-6">
//               <button
//                 onClick={() => setItemToDelete(null)}
//                 className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
//               >
//                 Annuler
//               </button>
//               <button
//                 onClick={async () => {
//                   await supabase
//                     .from("prospection_settings")
//                     .delete()
//                     .eq("id", itemToDelete);
//                   setItemToDelete(null);
//                   fetchProspection();
//                 }}
//                 className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
//               >
//                 Supprimer définitivement
//               </button>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default ProspectionSourcing;
