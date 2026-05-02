import {useState} from "react";
import axios from "axios";

export default function AiPanel({incident}) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleAsk() {
    setLoading(true);
    setError("");
    setResult(null);

    axios.post("http://localhost:5000/describe", {
      title: incident.title,
      description: incident.description,
    })
      .then((res) => {
        setResult(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log("AI service error:", err);
        setError("Failed to get AI response. Please try again.");
        setLoading(false);
      });
  }

  return (
    <div className="border border-gray-300 rounded p-4 mt-4">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold">AI Analysis</h2>
        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm disabled:opacity-50">
          {loading ? "Analysing..." : "Ask AI"}
        </button>
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <div className="w-4 h-4 border-2 border-purple-600 border-t-transparent rounded-full animate-spin" />
          Getting AI response...
        </div>
      )}

      {error && (
        <div className="text-sm text-red-500">
          <p>{error}</p>
          <button
            onClick={handleAsk}
            className="mt-2 text-purple-600 hover:underline text-xs">
            Retry
          </button>
        </div>
      )}

      {result && (
        <div className="mt-2 space-y-2">
          <p className="text-sm text-gray-700 whitespace-pre-line">{result.result}</p>
          <p className="text-xs text-gray-400">Generated at: {result.generated_at}</p>
        </div>
      )}
    </div>
  );
}