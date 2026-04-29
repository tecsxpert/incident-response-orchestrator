import {Navigate} from "react-router-dom";
import {useAuth} from "../components/AuthContext";

export default function ProtectedRoute({children}) {
  const {isAuthenticated} = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return children;
}