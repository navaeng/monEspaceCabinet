import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function CVUploadForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [addSkills, setAddSkills] = useState(null);
  const [englishCV, setEnglishCV] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [status, setStatus] = useState({ message: "", type: "" });

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

  const handleGenerate = async () => {
    if (!selectedFile || addSkills === null) {
      setStatus({
        message: "Veuillez sélectionner un fichier et choisir une option",
        type: "error",
      });
      return;
    }

    setIsGenerating(true);
    setStatus({ message: "", type: "" });

    try {
      const formData = new FormData();
      formData.append("cv", selectedFile);
      formData.append("add_skills", addSkills === "yes");
      formData.append("english_cv", englishCV);

      const response = await fetch(`${API_URL}/api/generate-dossier`, {
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
      setSelectedFile(null);
      setAddSkills(null);
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
    <div className="min-h-screen bg-white flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-md border border-gray-200 p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-base font-normal text-gray-900 mb-1">
            Génération de dossier
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

        {/* Skills Option */}
        <div className="mb-5">
          <label className="block text-xs font-normal text-gray-700 mb-2">
            Ajouter des compétences supplémentaires
          </label>
          <div className="flex gap-4">
            <div className="flex items-center">
              <input
                type="radio"
                id="skills-yes"
                checked={addSkills === "yes"}
                onChange={() => setAddSkills("yes")}
                disabled={!selectedFile}
                className="w-3 h-3 text-gray-900 border-gray-300 focus:ring-0 disabled:opacity-30"
              />
              <label
                htmlFor="skills-yes"
                className="ml-1.5 text-xs text-gray-700"
              >
                Oui
              </label>
            </div>
            <div className="flex items-center">
              <input
                type="radio"
                id="skills-no"
                checked={addSkills === "no"}
                onChange={() => setAddSkills("no")}
                disabled={!selectedFile}
                className="w-3 h-3 text-gray-900 border-gray-300 focus:ring-0 disabled:opacity-30"
              />
              <label
                htmlFor="skills-no"
                className="ml-1.5 text-xs text-gray-700"
              >
                Non
              </label>
            </div>
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
              disabled={!selectedFile}
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

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={!selectedFile || addSkills === null || isGenerating}
          className="w-full py-2 text-xs font-normal bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-30 disabled:cursor-not-allowed mb-4"
        >
          {isGenerating ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin mr-2 h-3 w-3 text-white"
                fill="none"
                viewBox="0 0 24 24"
              >
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
              </svg>
              Génération...
            </span>
          ) : (
            "Générer le dossier"
          )}
        </button>

        {/* Notice */}
        <div className="text-[10px] text-gray-500 border-t border-gray-100 pt-3">
          Le système peut commettre des erreurs. Vérifiez le dossier généré
          avant utilisation.
        </div>
      </div>
    </div>
  );
}

export default CVUploadForm;
