import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { supabase } from "../supabaseClient";

function Header() {
  // const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
    navigate("/Connexion");
  };

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user || null);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user || null);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

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

        <div className="hidden md:flex items-center space-x-4">
          {user && (
            <>
              <Link
                to="/Dashboard"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Tableau de bord
              </Link>
              <Link
                to="/"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Rechercher un candidat
              </Link>
              <Link
                to="/Prospection"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Prospection
              </Link>
              <Link
                to="/Dossier_competences"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Dossier de compétences
              </Link>
              {/* <Link
                to="/SignupUser"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Ajouter une personne
              </Link>*/}
              <Link
                to="EditInfos"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Modifier mes infos
              </Link>
              <Link
                to="/"
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Ajouter une personne
              </Link>
              <Link
                onClick={handleLogout}
                className="text-xs text-gray-600 hover:text-gray-900"
              >
                Déconnexion
              </Link>
            </>
          )}
        </div>

        <div className="hidden md:block">
          {!user && (
            <Link
              to="/Connexion"
              className="text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50"
            >
              Connexion
            </Link>
          )}
        </div>

        {/* {user ? (
            <button
              onClick={handleLogout}
              className="text-xs px-3 py-1.5 text-red-600 border border-red-200 rounded hover:bg-red-50"
            >
              Déconnexion
            </button>
          ) : (
            <Link
              to="/Connexion"
              className="text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50"
            >
              Connexion
            </Link>
          )}*/}
      </div>
    </header>
  );
}

export default Header;
