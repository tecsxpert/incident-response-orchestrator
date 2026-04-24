import {createContext, useState, useContext} from "react";

const AuthContext = createContext();

export function AuthProvider({children}) {
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  function login(newToken) {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{isAuthenticated, login, logout}}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}