// Payform.js - Version stylée
import React, { useState } from "react";
import { CardElement, useStripe, useElements } from "@stripe/react-stripe-js";

export default function Payform() {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handlePay = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      setError("Stripe n'est pas encore chargé");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // TODO: Appeler votre backend pour créer un Payment Intent
      // const { clientSecret } = await fetch('/api/payment').then(r => r.json());

      // Pour l'instant, juste un test
      console.log("✅ Paiement prêt !");
      setSuccess(true);

      // Simuler un délai
      setTimeout(() => {
        setSuccess(false);
      }, 3000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'DM Sans', sans-serif;
          background: #fafafa;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .payment-page {
          width: 100%;
          max-width: 500px;
          padding: 20px;
        }

        .payment-card {
          background: white;
          border-radius: 16px;
          padding: 40px 32px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }

        .payment-header {
          text-align: center;
          margin-bottom: 32px;
        }

        .payment-header h1 {
          font-size: 28px;
          font-weight: 700;
          color: #1a1a1a;
          margin-bottom: 8px;
        }

        .payment-header p {
          font-size: 15px;
          color: #737373;
        }

        .price-display {
          text-align: center;
          margin-bottom: 32px;
          padding: 24px;
          background: #f9f9f9;
          border-radius: 12px;
        }

        .price-amount {
          font-size: 48px;
          font-weight: 700;
          color: #1a1a1a;
          letter-spacing: -0.02em;
        }

        .price-period {
          font-size: 16px;
          color: #737373;
          margin-left: 4px;
        }

        .form-group {
          margin-bottom: 24px;
        }

        .form-label {
          display: block;
          font-size: 13px;
          font-weight: 600;
          color: #525252;
          margin-bottom: 8px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .card-element-wrapper {
          padding: 16px 20px;
          background: white;
          border: 1px solid #e5e5e5;
          border-radius: 8px;
          transition: all 0.2s ease;
        }

        .card-element-wrapper:focus-within {
          border-color: #1a1a1a;
          box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.1);
        }

        .alert {
          padding: 12px 16px;
          border-radius: 8px;
          margin-bottom: 16px;
          font-size: 14px;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .alert-error {
          background: #fee;
          color: #c00;
          border: 1px solid #fcc;
        }

        .alert-success {
          background: #e8f5e9;
          color: #2e7d32;
          border: 1px solid #c8e6c9;
        }

        .btn-primary {
          width: 100%;
          padding: 16px;
          background: #1a1a1a;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          font-family: 'DM Sans', sans-serif;
        }

        .btn-primary:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .btn-primary:disabled {
          background: #e5e5e5;
          color: #a3a3a3;
          cursor: not-allowed;
          transform: none;
        }

        .secure-badge {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          margin-top: 24px;
          padding: 16px;
          background: #f9f9f9;
          border-radius: 8px;
          color: #525252;
          font-size: 13px;
        }

        .spinner {
          display: inline-block;
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.6s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .features {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 16px;
          margin-top: 32px;
          padding-top: 32px;
          border-top: 1px solid #e5e5e5;
        }

        .feature {
          text-align: center;
        }

        .feature-icon {
          font-size: 24px;
          margin-bottom: 8px;
        }

        .feature-text {
          font-size: 12px;
          color: #737373;
        }
      `}</style>

      <div className="payment-page">
        <div className="payment-card">
          {/* Header */}
          <div className="payment-header">
            <h1>Paiement Sécurisé</h1>
            <p>Finalisez votre commande</p>
          </div>

          {/* Prix */}
          <div className="price-display">
            <span className="price-amount">25.00€</span>
            <span className="price-period">/ mois</span>
          </div>

          {/* Formulaire */}
          <form onSubmit={handlePay}>
            <div className="form-group">
              <label className="form-label">Informations de carte</label>
              <div className="card-element-wrapper">
                <CardElement
                  options={{
                    style: {
                      base: {
                        fontSize: "16px",
                        color: "#1a1a1a",
                        fontFamily: "DM Sans, sans-serif",
                        "::placeholder": {
                          color: "#a3a3a3",
                        },
                      },
                      invalid: {
                        color: "#c00",
                      },
                    },
                  }}
                />
              </div>
            </div>

            {/* Erreur */}
            {error && <div className="alert alert-error">⚠️ {error}</div>}

            {/* Succès */}
            {success && (
              <div className="alert alert-success">✅ Paiement réussi !</div>
            )}

            {/* Bouton */}
            <button
              type="submit"
              className="btn-primary"
              disabled={!stripe || loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  <span style={{ marginLeft: "8px" }}>Traitement...</span>
                </>
              ) : (
                "Payer 25.00€"
              )}
            </button>
          </form>

          {/* Badge sécurisé */}
          <div className="secure-badge">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span>Paiement 100% sécurisé par Stripe</span>
          </div>

          {/* Features */}
          <div className="features">
            <div className="feature">
              <div className="feature-icon">🔒</div>
              <div className="feature-text">Sécurisé</div>
            </div>
            <div className="feature">
              <div className="feature-icon">⚡</div>
              <div className="feature-text">Instantané</div>
            </div>
            <div className="feature">
              <div className="feature-icon">💳</div>
              <div className="feature-text">Toutes cartes</div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
