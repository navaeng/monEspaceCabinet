import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

export default function CVUploadForm() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleGenerate = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("cv", file);
      const res = await fetch(`${API_URL}/endpoint/generate_dossier`, { method: "POST", body: formData });
      if (!res.ok) throw new Error("Erreur génération");
      const blob = await res.blob();
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `dossier_de_competences${file.name}.docx`;
      a.click();
      setStatus("success");
    } catch (e) {
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={s.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700&family=DM+Sans:wght@300;400&display=swap');
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0%,100% { opacity: 0.4; } 50% { opacity: 1; } }
        .upload-label:hover { background: #1a1a1a !important; color: white !important; }
        .gen-btn:hover:not(:disabled) { background: #333 !important; }
      `}</style>

      {loading && (
        <div style={s.overlay}>
          <div style={s.spinner} />
          <p style={s.loadingText}>Analyse en cours...</p>
        </div>
      )}

      <div style={s.card}>
        <div style={s.eyebrow}>DOSSIER DE COMPÉTENCES</div>
        <h1 style={s.title}>Transformez<br/>votre CV</h1>
        <p style={s.sub}>Déposez votre fichier et laissez l'IA structurer votre dossier en quelques secondes.</p>

        <label className="upload-label" style={{ ...s.uploadBtn, opacity: loading ? 0.4 : 1, pointerEvents: loading ? "none" : "auto" }}>
          {file ? `📄 ${file.name}` : "Importer un CV"}
          <input type="file" accept=".pdf,.docx" disabled={loading} onChange={e => setFile(e.target.files[0])} style={{ display: "none" }} />
        </label>

        <button className="gen-btn" onClick={handleGenerate} disabled={!file || loading} style={{ ...s.genBtn, opacity: (!file || loading) ? 0.3 : 1 }}>
          Générer le dossier →
        </button>

        {status && (
          <p style={{ ...s.status, color: status === "success" ? "#2d6a4f" : "#c62828", animation: "fadeIn 0.3s ease" }}>
            {status === "success" ? "✓ Dossier téléchargé avec succès" : "✗ Erreur lors de la génération"}
          </p>
        )}
      </div>
    </div>
  );
}

const s = {
  page: { minHeight: "100vh", background: "#f5f0e8", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "'DM Sans', sans-serif" },
  overlay: { position: "fixed", inset: 0, background: "rgba(245,240,232,0.92)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", zIndex: 99, gap: "16px" },
  spinner: { width: "40px", height: "40px", border: "2px solid #ddd", borderTop: "2px solid #111", borderRadius: "50%", animation: "spin 0.8s linear infinite" },
  loadingText: { fontFamily: "'Syne', sans-serif", fontSize: "11px", letterSpacing: "0.2em", textTransform: "uppercase", color: "#666", animation: "pulse 2s ease infinite" },
  card: { background: "white", borderRadius: "24px", padding: "48px", width: "380px", boxShadow: "0 4px 40px rgba(0,0,0,0.08)", animation: "fadeIn 0.5s ease" },
  eyebrow: { fontFamily: "'Syne', sans-serif", fontSize: "9px", letterSpacing: "0.25em", color: "#aaa", marginBottom: "12px" },
  title: { fontFamily: "'Syne', sans-serif", fontSize: "36px", fontWeight: "700", lineHeight: 1.1, color: "#111", margin: "0 0 12px" },
  sub: { fontSize: "13px", color: "#888", lineHeight: 1.6, margin: "0 0 32px", fontWeight: "300" },
  uploadBtn: { display: "block", width: "100%", padding: "12px", fontSize: "12px", border: "1px solid #ddd", borderRadius: "10px", cursor: "pointer", textAlign: "center", background: "white", color: "#444", transition: "all 0.2s", marginBottom: "10px", boxSizing: "border-box" },
  genBtn: { width: "100%", padding: "14px", fontSize: "13px", background: "#111", color: "white", border: "none", borderRadius: "10px", cursor: "pointer", transition: "background 0.2s", fontFamily: "'Syne', sans-serif", letterSpacing: "0.05em" },
  status: { marginTop: "16px", fontSize: "12px", textAlign: "center" },
};