import {BrowserRouter, Routes, Route} from "react-router-dom";
import {AuthProvider} from "./components/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import IncidentList from "./pages/IncidentList";
import CreateIncident from "./pages/CreateIncident";
import EditIncident from "./pages/EditIncident";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import IncidentDetail from "./pages/IncidentDetail";
import Analytics from "./pages/Analytics";
import ErrorBoundary from "./components/ErrorBoundary";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route path="/" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Dashboard />
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/incidents" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <IncidentList />
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/create" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <CreateIncident />
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/edit/:id" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <EditIncident />
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/incidents/:id" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <IncidentDetail />
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/analytics" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Analytics />
              </ErrorBoundary>
            </ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}