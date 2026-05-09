import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function Navbar() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="bg-brand text-white px-6 py-3 flex justify-between items-center">
      <div className="flex items-center gap-8">
        <span className="font-bold text-lg tracking-wide">Incident Response</span>
        <div className="flex gap-6 text-sm">
          <button onClick={() => navigate("/")} className="hover:underline">Dashboard</button>
          <button onClick={() => navigate("/incidents")} className="hover:underline">Incidents</button>
          <button onClick={() => navigate("/analytics")} className="hover:underline">Analytics</button>
        </div>
      </div>
      <button
        onClick={handleLogout}
        className="text-sm border border-white px-3 py-1 rounded hover:bg-white hover:text-brand transition-colors">
        Logout
      </button>
    </nav>
  );
}