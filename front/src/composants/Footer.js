function Footer() {
  return (
    <>
      <style>{`
        .footer-link {
          color: #737373;
          text-decoration: none;
          font-size: 14px;
          transition: color 0.2s ease;
          display: block;
          margin-bottom: 12px;
        }

        .footer-link:hover {
          color: #1a1a1a;
        }

        .footer-title {
          font-size: 13px;
          font-weight: 600;
          color: #1a1a1a;
          margin-bottom: 16px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .social-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          border-radius: 8px;
          border: 1px solid #e5e5e5;
          background: white;
          color: #525252;
          transition: all 0.2s ease;
          text-decoration: none;
        }

        .social-icon:hover {
          background: #f5f5f5;
          border-color: #d4d4d4;
          color: #1a1a1a;
          transform: translateY(-2px);
        }

        @media (max-width: 768px) {
          .footer-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 32px !important;
          }

          .footer-brand {
            grid-column: 1 / -1;
          }
        }
      `}</style>

      <footer
        style={{
          background: "white",
          borderTop: "1px solid #e5e5e5",
          fontFamily: '"DM Sans", system-ui, -apple-system, sans-serif',
        }}
      >
        {/* Main Footer Content */}
        <div
          style={{
            maxWidth: "1200px",
            margin: "0 auto",
            padding: "64px 24px 32px",
          }}
        >
          <div
            className="footer-grid"
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(5, 1fr)",
              gap: "48px",
              marginBottom: "48px",
            }}
          >
            {/* Brand Column */}
            <div className="footer-brand" style={{ gridColumn: "span 2" }}>
              <div
                style={{
                  fontSize: "18px",
                  fontWeight: "700",
                  color: "#1a1a1a",
                  marginBottom: "12px",
                  letterSpacing: "-0.01em",
                }}
              >
                Recrutement
              </div>
              <p
                style={{
                  fontSize: "14px",
                  color: "#737373",
                  lineHeight: "1.6",
                  marginBottom: "20px",
                  maxWidth: "280px",
                }}
              >
                La plateforme moderne pour automatiser et optimiser votre
                processus de recrutement.
              </p>

              {/* Social Icons */}
              <div style={{ display: "flex", gap: "8px" }}>
                <a href="#" className="social-icon" aria-label="LinkedIn">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                  </svg>
                </a>
                <a href="#" className="social-icon" aria-label="Twitter">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                  </svg>
                </a>
                <a href="#" className="social-icon" aria-label="GitHub">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                </a>
              </div>
            </div>

            {/* Product Column */}
            <div>
              <div className="footer-title">Produit</div>
              <a href="#fonctionnalites" className="footer-link">
                Fonctionnalités
              </a>
              <a href="#tarifs" className="footer-link">
                Tarifs
              </a>
              <a href="#integrations" className="footer-link">
                Intégrations
              </a>
              <a href="#changelog" className="footer-link">
                Changelog
              </a>
            </div>

            {/* Company Column */}
            <div>
              <div className="footer-title">Entreprise</div>
              <a href="#apropos" className="footer-link">
                À propos
              </a>
              <a href="#blog" className="footer-link">
                Blog
              </a>
              <a href="#carriere" className="footer-link">
                Carrière
              </a>
              <a href="#contact" className="footer-link">
                Contact
              </a>
            </div>

            {/* Resources Column */}
            <div>
              <div className="footer-title">Ressources</div>
              <a href="#documentation" className="footer-link">
                Documentation
              </a>
              <a href="#support" className="footer-link">
                Support
              </a>
              <a href="#api" className="footer-link">
                API
              </a>
              <a href="#statut" className="footer-link">
                Statut
              </a>
            </div>
          </div>

          {/* Bottom Bar */}
          <div
            style={{
              paddingTop: "32px",
              borderTop: "1px solid #e5e5e5",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "16px",
            }}
          >
            <p
              style={{
                fontSize: "13px",
                color: "#a3a3a3",
                margin: 0,
              }}
            >
              © 2026 Recrutement. Tous droits réservés.
            </p>

            <div
              style={{
                display: "flex",
                gap: "24px",
                flexWrap: "wrap",
              }}
            >
              <a
                href="#confidentialite"
                style={{
                  fontSize: "13px",
                  color: "#a3a3a3",
                  textDecoration: "none",
                  transition: "color 0.2s ease",
                }}
                onMouseEnter={(e) => (e.target.style.color = "#525252")}
                onMouseLeave={(e) => (e.target.style.color = "#a3a3a3")}
              >
                Confidentialité
              </a>
              <a
                href="#conditions"
                style={{
                  fontSize: "13px",
                  color: "#a3a3a3",
                  textDecoration: "none",
                  transition: "color 0.2s ease",
                }}
                onMouseEnter={(e) => (e.target.style.color = "#525252")}
                onMouseLeave={(e) => (e.target.style.color = "#a3a3a3")}
              >
                Conditions
              </a>
              <a
                href="#cookies"
                style={{
                  fontSize: "13px",
                  color: "#a3a3a3",
                  textDecoration: "none",
                  transition: "color 0.2s ease",
                }}
                onMouseEnter={(e) => (e.target.style.color = "#525252")}
                onMouseLeave={(e) => (e.target.style.color = "#a3a3a3")}
              >
                Cookies
              </a>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}

export default Footer;
