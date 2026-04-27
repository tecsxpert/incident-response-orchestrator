import {BrowserRouter, Routes, Route} from "react-router-dom";
import {AuthProvider} from "./components/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import IncidentList from "./pages/IncidentList";
import CreateIncident from "./pages/CreateIncident";
import EditIncident from "./pages/EditIncident";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/incidents" element={<ProtectedRoute><IncidentList /></ProtectedRoute>} />
          <Route path="/create" element={<ProtectedRoute><CreateIncident /></ProtectedRoute>} />
          <Route path="/edit/:id" element={<ProtectedRoute><EditIncident /></ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}