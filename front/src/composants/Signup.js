import { useState, useRef, useEffect } from "react";
import { supabase } from "../supabaseClient";
import { useNavigate } from "react-router-dom";

function Signup({ onBack }) {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const [formData, setFormData] = useState({
    nom: "",
    siren: "",
    adresse: "",
    codePostal: "",
    ville: "",
    pays: "France",
    telephone: "",
    email: "",
    motDePasse: "",
    confirmMotDePasse: "",
  });

  const wrapperRef = useRef(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleChange = async (e) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);

    if (!value || value.length < 2) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      setIsOpen(true);
      try {
        const url = `https://recherche-entreprises.api.gouv.fr/search?q=${encodeURIComponent(value)}&page=1&per_page=10`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        setResults(data.results || []);
      } catch (err) {
        console.error("❌ Erreur:", err);
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 300);
  };

  const handleSelect = (cabinet) => {
    const nom = cabinet.nom_complet || cabinet.nom_raison_sociale || "";
    const adresse = cabinet.siege?.adresse || "";
    const ville = cabinet.siege?.commune || "";
    const codePostal = cabinet.siege?.code_postal || "";

    setQuery(nom);
    setFormData({
      nom,
      siren: cabinet.siren || "",
      adresse,
      codePostal,
      ville,
      pays: "France",
      telephone: "",
      email: "",
    });

    setResults([]);
    setIsOpen(false);
  };

  const handleKeyDown = (e) => {
    if (!isOpen || results.length === 0) return;

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setSelectedIndex((prev) =>
          prev < results.length - 1 ? prev + 1 : prev,
        );
        break;
      case "ArrowUp":
        e.preventDefault();
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1));
        break;
      case "Enter":
        e.preventDefault();
        if (selectedIndex >= 0) handleSelect(results[selectedIndex]);
        break;
      case "Escape":
        setIsOpen(false);
        break;
      default:
        break;
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 1️⃣ Créer un compte utilisateur avec email/mot de passe
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: formData.email,
        password: formData.motDePasse,
        options: {
          data: {
            nom_cabinet: formData.nom,
            siren: formData.siren,
          },
        },
      });

      if (authError) throw authError;

      const { data, error } = await supabase
        .from("cabinets")
        .insert([
          {
            user_id: authData.user.id,
            nom: formData.nom,
            siren: formData.siren,
            adresse: formData.adresse,
            code_postal: formData.codePostal,
            ville: formData.ville,
            pays: formData.pays,
            telephone: formData.telephone,
            email: formData.email,
          },
        ])
        .select();

      if (error) {
        throw error;
      }

      console.log("✅ Cabinet enregistré:", data);
      alert("Inscription réussie !");

      handleReset();
      navigate("/Dashboard");

      if (onBack) onBack();
    } catch (error) {
      console.error("❌ Erreur:", error);

      if (error.code === "23505") {
        alert("Ce SIREN existe déjà dans la base de données");
      } else {
        alert(`Erreur: ${error.message}`);
      }
    }
  };

  const handleReset = () => {
    setQuery("");
    setFormData({
      nom: "",
      siren: "",
      adresse: "",
      codePostal: "",
      ville: "",
      pays: "France",
      telephone: "",
      email: "",
    });
  };

  return (
    <div
      style={{
        fontFamily: '"DM Sans", system-ui, -apple-system, sans-serif',
        minHeight: "100vh",
        background: "#fafafa",
      }}
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        .modern-input {
          width: 100%;
          padding: 12px 16px;
          font-size: 15px;
          border: 1px solid #e5e5e5;
          border-radius: 8px;
          background: white;
          color: #1a1a1a;
          transition: all 0.2s ease;
          font-family: inherit;
        }

        .modern-input:focus {
          outline: none;
          border-color: #a3a3a3;
          box-shadow: 0 0 0 3px rgba(163, 163, 163, 0.1);
        }

        .modern-input:read-only {
          background: #f9f9f9;
          color: #737373;
        }

        .modern-label {
          display: block;
          font-size: 13px;
          font-weight: 500;
          color: #525252;
          margin-bottom: 8px;
          letter-spacing: 0.01em;
        }

        .modern-btn {
          padding: 12px 24px;
          font-size: 15px;
          font-weight: 500;
          border-radius: 8px;
          border: 1px solid #e5e5e5;
          cursor: pointer;
          transition: all 0.2s ease;
          font-family: inherit;
        }

        .btn-primary-form {
          background: #1a1a1a;
          color: white;
          border-color: #1a1a1a;
          width: 100%;
        }

        .btn-primary-form:hover {
          background: #2a2a2a;
          transform: translateY(-1px);
        }

        .btn-secondary-form {
          background: white;
          color: #525252;
          border-color: #e5e5e5;
          width: 100%;
        }

        .btn-secondary-form:hover {
          background: #f5f5f5;
          border-color: #d4d4d4;
        }

        .dropdown-item-modern {
          padding: 16px;
          border-bottom: 1px solid #f5f5f5;
          cursor: pointer;
          transition: background 0.15s ease;
        }

        .dropdown-item-modern:hover,
        .dropdown-item-modern.active {
          background: #f9f9f9;
        }

        .dropdown-item-modern.active {
          background: #1a1a1a;
          color: white;
        }

        .back-link {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          color: #525252;
          text-decoration: none;
          font-size: 14px;
          font-weight: 500;
          transition: color 0.2s ease;
        }

        .back-link:hover {
          color: #1a1a1a;
        }
      `}</style>

      <div
        style={{ maxWidth: "600px", margin: "0 auto", padding: "60px 24px" }}
      >
        <div
          style={{
            background: "white",
            border: "1px solid #e5e5e5",
            borderRadius: "12px",
            padding: "40px",
            marginTop: "24px",
          }}
        >
          <div style={{ marginBottom: "32px" }}>
            <h1
              style={{
                fontSize: "28px",
                fontWeight: "700",
                marginBottom: "8px",
                color: "#1a1a1a",
                letterSpacing: "-0.02em",
              }}
            >
              Inscription Cabinet
            </h1>
            <p style={{ fontSize: "15px", color: "#737373" }}>
              Complétez les informations de votre cabinet
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Recherche */}
            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">Rechercher votre cabinet *</label>
              <div ref={wrapperRef} style={{ position: "relative" }}>
                <input
                  type="text"
                  className="modern-input"
                  placeholder="Tapez le nom du cabinet..."
                  value={query}
                  onChange={handleChange}
                  onKeyDown={handleKeyDown}
                  onFocus={() => query && query.length >= 2 && setIsOpen(true)}
                  autoComplete="off"
                  required
                />

                {isOpen && (
                  <div
                    style={{
                      position: "absolute",
                      top: "100%",
                      left: 0,
                      right: 0,
                      marginTop: "8px",
                      maxHeight: "320px",
                      overflowY: "auto",
                      zIndex: 1000,
                      background: "white",
                      border: "1px solid #e5e5e5",
                      borderRadius: "8px",
                      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.08)",
                    }}
                  >
                    {loading && (
                      <div
                        style={{
                          padding: "24px",
                          textAlign: "center",
                          color: "#737373",
                          fontSize: "14px",
                        }}
                      >
                        Recherche en cours...
                      </div>
                    )}

                    {!loading && results.length === 0 && (
                      <div
                        style={{
                          padding: "24px",
                          textAlign: "center",
                          color: "#737373",
                          fontSize: "14px",
                        }}
                      >
                        Aucun résultat trouvé
                      </div>
                    )}

                    {!loading && results.length > 0 && (
                      <div>
                        {results.map((cabinet, index) => {
                          const nom =
                            cabinet.nom_complet ||
                            cabinet.nom_raison_sociale ||
                            "Sans nom";
                          const adresse = cabinet.siege?.adresse || "";
                          const ville = cabinet.siege?.commune || "";
                          const codePostal = cabinet.siege?.code_postal || "";

                          return (
                            <div
                              key={cabinet.siren || index}
                              className={`dropdown-item-modern ${index === selectedIndex ? "active" : ""}`}
                              onClick={() => handleSelect(cabinet)}
                              onMouseEnter={() => setSelectedIndex(index)}
                            >
                              <div
                                style={{
                                  fontWeight: "500",
                                  fontSize: "15px",
                                  marginBottom: "4px",
                                  color:
                                    index === selectedIndex
                                      ? "white"
                                      : "#1a1a1a",
                                }}
                              >
                                {nom}
                              </div>
                              {(adresse || ville) && (
                                <div
                                  style={{
                                    fontSize: "13px",
                                    color:
                                      index === selectedIndex
                                        ? "rgba(255,255,255,0.7)"
                                        : "#737373",
                                  }}
                                >
                                  {adresse && <span>{adresse}</span>}
                                  {adresse && (ville || codePostal) && (
                                    <span> • </span>
                                  )}
                                  {codePostal && <span>{codePostal} </span>}
                                  {ville && <span>{ville}</span>}
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>
              <div
                style={{ fontSize: "13px", color: "#a3a3a3", marginTop: "8px" }}
              >
                Tapez au moins 2 caractères pour rechercher
              </div>
            </div>

            {/* Nom */}
            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">Nom du cabinet *</label>
              <input
                type="text"
                className="modern-input"
                name="nom"
                value={formData.nom}
                onChange={handleInputChange}
                required
                readOnly
              />
            </div>

            {/* SIREN */}
            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">SIREN *</label>
              <input
                type="text"
                className="modern-input"
                name="siren"
                value={formData.siren}
                onChange={handleInputChange}
                required
                readOnly
              />
            </div>

            {/* Adresse */}
            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">Adresse *</label>
              <input
                type="text"
                className="modern-input"
                name="adresse"
                value={formData.adresse}
                onChange={handleInputChange}
                required
                readOnly
              />
            </div>

            {/* Code postal et Ville */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 2fr",
                gap: "16px",
                marginBottom: "24px",
              }}
            >
              <div>
                <label className="modern-label">Code postal *</label>
                <input
                  type="text"
                  className="modern-input"
                  name="codePostal"
                  value={formData.codePostal}
                  onChange={handleInputChange}
                  required
                  readOnly
                />
              </div>
              <div>
                <label className="modern-label">Ville *</label>
                <input
                  type="text"
                  className="modern-input"
                  name="ville"
                  value={formData.ville}
                  onChange={handleInputChange}
                  required
                  readOnly
                />
              </div>
            </div>

            {/* Pays */}
            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">Pays *</label>
              <input
                type="text"
                className="modern-input"
                name="pays"
                value={formData.pays}
                onChange={handleInputChange}
                required
                readOnly
              />
            </div>

            {/* Téléphone */}
            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">Téléphone *</label>
              <input
                type="tel"
                className="modern-input"
                name="telephone"
                value={formData.telephone}
                onChange={handleInputChange}
                placeholder="01 23 45 67 89"
                required
              />
            </div>

            {/* Email */}
            <div style={{ marginBottom: "32px" }}>
              <label className="modern-label">Email *</label>
              <input
                type="email"
                className="modern-input"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="contact@cabinet.fr"
                required
              />
            </div>

            <div style={{ marginBottom: "24px" }}>
              <label className="modern-label">Mot de passe *</label>
              <input
                type="password"
                className="modern-input"
                name="motDePasse"
                value={formData.motDePasse}
                onChange={handleInputChange}
                placeholder="Minimum 6 caractères"
                required
                minLength="6"
              />
            </div>

            <div style={{ marginBottom: "32px" }}>
              <label className="modern-label">
                Confirmer le mot de passe *
              </label>
              <input
                type="password"
                className="modern-input"
                name="confirmMotDePasse"
                value={formData.confirmMotDePasse}
                onChange={handleInputChange}
                placeholder="Répétez le mot de passe"
                required
              />
            </div>

            {/* Boutons */}
            <div
              style={{ display: "flex", flexDirection: "column", gap: "12px" }}
            >
              <button type="submit" className="modern-btn btn-primary-form">
                S'inscrire
              </button>
              <button
                type="button"
                className="modern-btn btn-secondary-form"
                onClick={handleReset}
              >
                Réinitialiser
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Signup;
