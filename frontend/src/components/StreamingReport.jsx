import {useState} from "react";

export default function StreamingReport({ incidentId }) {
  const [report, setReport] = useState("");
  const [streaming, setStreaming] = useState(false);

  function handleGenerate() {
    setReport("");
    setStreaming(true);

    const source = new EventSource(`http://localhost:5000/generate-report?id=${incidentId}`);

    source.onmessage = (e) => {
      setReport((prev) => prev + e.data);
    };

    source.onerror = () => {
      setStreaming(false);
      source.close();
    };

    source.addEventListener("done", () => {
      setStreaming(false);
      source.close();
    });
  }

  return (
    <div className="border border-gray-300 rounded p-4 mt-4">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold">AI Report</h2>
        <button
          onClick={handleGenerate}
          disabled={streaming}
          className="bg-brand hover:bg-brand text-white px-4 py-2 rounded text-sm min-h-[44px] disabled:opacity-50">
          {streaming ? "Generating..." : "Generate Report"}
        </button>
      </div>

      {report && (
        <div className="text-sm text-gray-700 whitespace-pre-line mt-2">
          {report}
          {streaming && <span className="animate-pulse">▍</span>}
        </div>
      )}

      {!report && !streaming && (
        <p className="text-sm text-gray-400">Click Generate Report to get an AI summary.</p>
      )}
    </div>
  );
}