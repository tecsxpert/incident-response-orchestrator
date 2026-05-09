import {useState} from "react";
import {useNavigate} from "react-router-dom";
import api from "../services/api";
import {useAuth} from "../components/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const {login} = useAuth();

  const [form, setForm] = useState({ username: "", password: "" });
  const [errors, setErrors] = useState({});
  const [error, setError] = useState("");

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  }

  function validate() {
    const newErrors = {};
    if (!form.username.trim()) newErrors.username = "Username is required";
    if (!form.password.trim()) newErrors.password = "Password is required";
    return newErrors;
  }

  function handleSubmit(e) {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    api.post("/auth/login", form)
      .then((res) => {
        login(res.data.token);
        navigate("/");
      })
      .catch((err) => {
        console.log("Login error:", err);
        setError("Invalid username or password");
      });
  }

  return (
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <div className="w-full max-w-sm">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-brand">Incident Response</h1>
        <p className="text-gray-400 text-sm mt-2">Orchestrator Platform</p>
      </div>

      <div className="bg-white rounded-xl shadow-md p-8 border border-gray-100">
        <h2 className="text-xl font-semibold text-gray-800 mb-6 text-center">Sign in</h2>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded px-3 py-2 mb-4">
            <p className="text-red-500 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand"
            />
            {errors.username && <p className="text-red-500 text-xs mt-1">{errors.username}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand"
            />
            {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password}</p>}
          </div>

          <button
            type="submit"
            className="w-full bg-brand hover:bg-blue-900 text-white px-4 py-3 rounded-lg text-sm font-medium min-h-[44px] transition-colors mt-2">
            Sign In
          </button>
        </form>
      </div>
    </div>
  </div>
);
}