import { useState } from "react";
import { Link } from "react-router-dom";

function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200 font-sans">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        {/* Logo */}
        <Link
          to="/"
          className="text-sm font-normal text-gray-900 hover:text-gray-700"
        >
          Acceuil
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-4">
          <Link
            to="/dashboard"
            className="text-xs text-gray-600 hover:text-gray-900"
          >
            Tableau de bord
          </Link>
        </div>

        {/* Desktop Actions */}
        <div className="hidden md:block">
          <Link
            to="/Connexion"
            className="text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50"
          >
            Connexion
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden p-1"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? (
            <span className="text-xs text-gray-600">✕</span>
          ) : (
            <span className="text-xs text-gray-600">☰</span>
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-4 py-3 space-y-3">
            <Link
              to="/Dashboard"
              className="block text-xs text-gray-600 hover:text-gray-900 py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              Tableau de bord
            </Link>
            <Link
              to="/Connexion"
              className="block text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 text-center"
              onClick={() => setMobileMenuOpen(false)}
            >
              Connexion
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;
