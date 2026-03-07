import { useState } from "react";
const API_URL = "http://127.0.0.1:8000";
// const API_URL = "https://filltemplate.onrender.com";
function CVUploadForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [addSkills, setAddSkills] = useState(null);
  const [englishCV, setEnglishCV] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [status, setStatus] = useState({ message: "", type: "" });
  const [extraInstructions, setExtraInstructions] = useState("");
  const [wasGenerated, setWasGenerated] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      const validTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ];

      if (!validTypes.includes(file.type)) {
        return;
      }

      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        return;
      }

      setSelectedFile(file);
      setAddSkills(null);
      setEnglishCV(false);
    }
  };

  const handleGenerate = async (model = "openai/gpt-oss-120b") => {
    if (!selectedFile) {
      setStatus({
        message: "Veuillez sélectionner un fichier et choisir une option",
        type: "error",
      });
      return;
    }
    try {
      setIsGenerating(true);
      setStatus({ message: "", type: "" });

      const formData = new FormData();
      formData.append("cv", selectedFile);

      console.log(extraInstructions);

      const response = await fetch(`${API_URL}/endpoint/generate_dossier`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Erreur lors de la génération");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `dossier_${selectedFile.name.replace(/\.(pdf|docx)$/i, "")}.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setStatus({
        message: "Dossier généré et téléchargé avec succès.",
        type: "success",
      });
      setWasGenerated(model !== "hermes-405b");
      setEnglishCV(false);
    } catch (error) {
      console.error("Erreur lors de la génération:", error);
      setStatus({
        message: error.message || "Erreur lors de la génération",
        type: "error",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-50 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-md border border-black-200 p-6 bg-slate-50 rounded-[2rem]">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-base font-normal text-black-900 mb-1">
            Dossier de compétences
          </h1>

          <p className="text-xs text-gray-500">
            Téléchargez votre CV pour générer automatiquement votre dossier
          </p>
        </div>

        {/* File Upload */}
        <div className="mb-5">
          <label className="block text-xs font-normal text-gray-700 mb-2">
            Fichier CV
          </label>
          <div className="relative">
            <input
              type="file"
              id="cv-file"
              accept=".pdf,.docx"
              onChange={handleFileSelect}
              className="hidden"
              disabled={isGenerating}
            />
            <label
              htmlFor="cv-file"
              className="block w-full px-3 py-2 text-xs border border-gray-300 rounded cursor-pointer hover:border-gray-400 transition-colors"
            >
              {selectedFile ? selectedFile.name : "Sélectionner un fichier"}
            </label>
            {selectedFile && (
              <p className="text-xs text-gray-500 mt-1">
                {(selectedFile.size / 1024).toFixed(0)} Ko
              </p>
            )}
          </div>
        </div>

        {/* English Option */}
        <div className="mb-6">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="english"
              checked={englishCV}
              onChange={(e) => setEnglishCV(e.target.checked)}
              disabled={isGenerating}
              className="w-3 h-3 text-gray-900 border-gray-300 rounded focus:ring-0 disabled:opacity-30"
            />
            <label htmlFor="english" className="ml-1.5 text-xs text-gray-700">
              CV anglais
            </label>
          </div>
        </div>

        {/* Status Message */}
        {status.message && (
          <div className="mb-4 p-3 text-xs border rounded">
            <p
              className={
                status.type === "error"
                  ? "text-red-700"
                  : status.type === "success"
                    ? "text-green-700"
                    : "text-gray-700"
              }
            >
              {status.message}
            </p>
          </div>
        )}
        {wasGenerated && (
          <button
            disabled={isGenerating}
            onClick={() => handleGenerate("hermes-405b")}
            className="w-full py-2 text-xs font-normal border border-black text-black rounded hover:bg-gray-100 transition-colors mb-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Mauvais résultat ? Regénérer avec le modèle llama 450b
          </button>
        )}

        {isGenerating && (
          <div className="w-full max-w-xs mx-auto py-8 flex flex-col items-center gap-3">
            {/* La barre de scan ultra fine */}
            <div className="relative w-full h-[2px] bg-gray-100 overflow-hidden">
              <div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-900 to-transparent animate-shimmer"
                style={{ width: "50%", backgroundSize: "200% 100%" }}
              />
            </div>
            {/* Texte minimaliste */}
            <span className="text-[10px] uppercase tracking-[0.3em] font-medium text-gray-500 animate-pulse">
              Chargement...
            </span>
            <style>{`
              @keyframes shimmer {
                0% { transform: translateX(-150%); }
                100% { transform: translateX(250%); }
              }
              .animate-shimmer { animation: shimmer 1.5s infinite linear; }
            `}</style>
          </div>
        )}
        <div classname="mb-5">
          <label className="block text-xs font-normal text-gray-700 mb-2">
            Instructions complémentaires (optionnel)
          </label>
          <textarea
            value={extraInstructions}
            onChange={(e) => setExtraInstructions(e.target.value)}
            disabled={isGenerating}
            placeholder="Exemple : Ajoute une expériences en plus qui n'est pas
          mentionnée..."
            className="w-full px-3 py-2 text-xs border
          border-gray-300 rounded resize-none focus:outline-none
            focus:border-gray-400 disabled:opacity-30"
            rows={3}
          />
        </div>

        {/* Generate Button */}
        <button
          onClick={() => handleGenerate()}
          disabled={!selectedFile || isGenerating}
          className="w-full py-2 text-xs font-normal bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-30 disabled:cursor-not-allowed mb-4"
        >
          Générer le dossier
        </button>
      </div>
    </div>
  );
}

export default CVUploadForm;
