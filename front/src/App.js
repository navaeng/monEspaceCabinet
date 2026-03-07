import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./composants/Dashboard";
import CVUploadForm from "./composants/dossier_competences";
import ProspectionSourcing from "./composants/ProspectionSourcing";
import Header from "./composants/Header";
import Login from "./composants/Login";
import Home from "./composants/Home";
import ProtectedRoute from "./composants/ProtectedRoute";
import { useState, useEffect } from "react";
import { supabase } from "./supabaseClient";
import EditInfos from "./composants/EditInfos";
import RechercheCandidat from "./composants/RechercheCandidat";
import EmailAuto from "./composants/EmailAuto";
import AjouterPersonne from "./composants/AjouterPersonne";
// import SignupUser from "./composants/SignupUser";
import Discussion from "./composants/Discussion";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });
  }, []);

  return (
    <BrowserRouter>
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        {
          <Route
            path="/ProspectionSourcing"
            element={
              <ProtectedRoute>
                <ProspectionSourcing />
              </ProtectedRoute>
            }
          />
        }
        <Route
          path="/RechercheCandidat"
          element={
            <ProtectedRoute>
              <RechercheCandidat />
            </ProtectedRoute>
          }
        />
        <Route
          path="/EmailAuto"
          element={
            <ProtectedRoute>
              <EmailAuto />
            </ProtectedRoute>
          }
        />
        <Route
          path="/AjouterPersonne"
          element={
            <ProtectedRoute>
              <AjouterPersonne />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Disscussion"
          element={
            <ProtectedRoute>
              <Discussion />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Connexion"
          element={<Login onLoginSuccess={(u) => setUser(u)} />}
        />
        {
          <Route
            path="/Dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        }
        {/* <Route path="/dossier_competences" element={<CVUploadForm />} />*/}
        <Route
          path="/dossier_competences"
          element={
            <ProtectedRoute>
              <CVUploadForm />
            </ProtectedRoute>
          }
        />
        <Route
          path="/EditInfos"
          element={
            <ProtectedRoute>
              <EditInfos />
            </ProtectedRoute>
          }
        />
        {/* <Route
          path="/SignupUser"
          element={
            <ProtectedRoute>
              <SignupUser />
            </ProtectedRoute>
          }
        />*/}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
