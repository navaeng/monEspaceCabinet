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
// import SignupUser from "./composants/SignupUser";

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
