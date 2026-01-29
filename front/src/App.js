import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./composants/Dashboard";
import CVUploadForm from "./composants/dossier_competences";
import Prospection from "./composants/Prospection";
import Header from "./composants/Header";
import Login from "./composants/Login";
//import Home from "./composants/Home";
//import ProtectedRoute from "./composants/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Header />

      <Routes>
        <Route path="/" element={<Prospection />} />
        {/* <Route
          path="/Prospection"
          element={
            <ProtectedRoute>
              <Prospection />
            </ProtectedRoute>
          }
        />*/}
        {/* <Route
          path="/Dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />*/}
        <Route path="/dossier_competences" element={<CVUploadForm />} />
        <Route path="/Connexion" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
