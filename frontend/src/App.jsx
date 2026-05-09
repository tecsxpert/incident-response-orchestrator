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
import Navbar from "./components/Navbar";

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto">
        {children}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route path="/" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Layout><Dashboard /></Layout>
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/incidents" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Layout><IncidentList /></Layout>
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/create" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Layout><CreateIncident /></Layout>
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/edit/:id" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Layout><EditIncident /></Layout>
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/incidents/:id" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Layout><IncidentDetail /></Layout>
              </ErrorBoundary>
            </ProtectedRoute>
          } />

          <Route path="/analytics" element = {
            <ProtectedRoute>
              <ErrorBoundary>
                <Layout><Analytics /></Layout>
              </ErrorBoundary>
            </ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}