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
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-sm p-6 border border-gray-300 rounded">
        <h1 className="text-2xl font-bold mb-4">Login</h1>

        {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm font-medium">Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm" />
              {errors.username && <p className="text-red-500 text-xs mt-1">{errors.username}</p>}
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium">Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm" />
              {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password}</p>}
          </div>

          <button
            type="submit"
            className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}