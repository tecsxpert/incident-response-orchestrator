import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import api from "../services/api";
import AiPanel from "../components/AiPanel";
import StreamingReport from "../components/StreamingReport";

const mockIncident = {
  id: 1,
  title: "Database connection timeout",
  description: "The database is not responding to connection requests from the application server.",
  priority: "CRITICAL",
  status: "OPEN",
  assignedTo: "Ravi",
  createdBy: "Karthik",
  createdAt: "2026-04-15",
  updatedAt: "2026-04-16",
  aiAnalysis: "This incident appears to be caused by a network misconfiguration or database overload. Recommend checking connection pool settings and database server logs immediately.",
};

const priorityColors = {
  LOW: "bg-green-100 text-green-700",
  MEDIUM: "bg-yellow-100 text-yellow-700",
  HIGH: "bg-orange-100 text-orange-700",
  CRITICAL: "bg-red-100 text-red-700",
};

const statusColors = {
  OPEN: "bg-blue-100 text-blue-700",
  IN_PROGRESS: "bg-purple-100 text-purple-700",
  RESOLVED: "bg-green-100 text-green-700",
};

export default function IncidentDetail() {
  const {id} = useParams();
  const navigate = useNavigate();
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/incidents/${id}`)
      .then((res) => {
        setIncident({ ...mockIncident, id: Number(id) });
        setLoading(false);
      })
      .catch((err) => {
      console.log("Error fetching incident:", err);
      const mockData = {
        1: { id: 1, title: "Database connection timeout", description: "The database is not responding to connection requests.", priority: "CRITICAL", status: "OPEN", assignedTo: "Ravi", createdBy: "Karthik", createdAt: "2026-04-15", updatedAt: "2026-04-16" },
        2: { id: 2, title: "API response delay on /orders", description: "API response time exceeded 5 seconds on the orders endpoint.", priority: "HIGH", status: "IN_PROGRESS", assignedTo: "Priya", createdBy: "Ravi", createdAt: "2026-04-14", updatedAt: "2026-04-15" },
        3: { id: 3, title: "Memory usage above 85%", description: "Server memory usage has crossed 85% threshold.", priority: "MEDIUM", status: "RESOLVED", assignedTo: "Karthik", createdBy: "Priya", createdAt: "2026-04-13", updatedAt: "2026-04-14" },
     };
     setIncident(mockData[Number(id)] || mockData[1]);
     setLoading(false);
   });
  }, [id]);

  function handleDelete() {
    if (!window.confirm("Are you sure you want to delete this incident?")) return;
    api.delete(`/incidents/${id}`)
      .then(() => navigate("/incidents"))
      .catch((err) => console.log("Error deleting incident:", err));
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="h-8 bg-gray-200 rounded animate-pulse mb-4 w-1/3" />
        <div className="h-4 bg-gray-200 rounded animate-pulse mb-2" />
        <div className="h-4 bg-gray-200 rounded animate-pulse mb-2" />
        <div className="h-4 bg-gray-200 rounded animate-pulse w-2/3" />
      </div>
    );
  }

  if (!incident) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Incident Detail</h1>
        <div className="text-center py-16">
          <p className="text-gray-400 text-lg">Incident not found.</p>
          <p className="text-gray-300 text-sm mt-1">It may have been deleted or does not exist.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <button
        onClick={() => navigate("/incidents")}
        className="text-sm text-brand hover:underline mb-4 block">
        ← Back to Incidents
      </button>

      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">{incident.title}</h1>
          <p className="text-sm text-gray-400 mt-1">Incident #{incident.id}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => navigate(`/edit/${incident.id}`)}
            className="bg-brand hover:bg-blue-900 text-white px-4 py-2 rounded text-sm min-h-[44px]">
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm min-h-[44px]">
            Delete
          </button>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm mb-4 border-l-4 border-l-brand hover:shadow-md transition-shadow">
        <div className="flex gap-2 mb-4">
          <span className={`px-2 py-1 rounded text-xs font-medium ${priorityColors[incident.priority]}`}>
            {incident.priority}
          </span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[incident.status]}`}>
            {incident.status}
          </span>
        </div>

        <div className="mb-4">
          <p className="text-sm text-gray-500 mb-1">Description</p>
          <p className="text-sm text-gray-700">{incident.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Assigned To</p>
            <p className="text-sm font-medium">{incident.assignedTo}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Created By</p>
            <p className="text-sm font-medium">{incident.createdBy}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Created At</p>
            <p className="text-sm font-medium">{incident.createdAt}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Updated At</p>
            <p className="text-sm font-medium">{incident.updatedAt}</p>
          </div>
        </div>
      </div>

      <AiPanel incident={incident} />
      <StreamingReport incidentId={incident.id} />
    </div>
  );
}