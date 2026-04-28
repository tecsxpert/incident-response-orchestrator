import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import api from "../services/api";

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
        setIncident(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log("Error fetching incident:", err);
        setIncident(mockIncident);
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

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{incident.title}</h1>
        <div className="flex gap-2">
          <button
            onClick={() => navigate(`/edit/${incident.id}`)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm">
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm">
            Delete
          </button>
        </div>
      </div>

      <div className="border border-gray-300 rounded p-4 mb-4 space-y-3">
        <div className="flex gap-2">
          <span className={`px-2 py-1 rounded text-xs font-medium ${priorityColors[incident.priority]}`}>
            {incident.priority}
          </span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[incident.status]}`}>
            {incident.status}
          </span>
        </div>

        <div>
          <p className="text-sm text-gray-500">Description</p>
          <p className="text-sm">{incident.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Assigned To</p>
            <p className="text-sm">{incident.assignedTo}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Created By</p>
            <p className="text-sm">{incident.createdBy}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Created At</p>
            <p className="text-sm">{incident.createdAt}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Updated At</p>
            <p className="text-sm">{incident.updatedAt}</p>
          </div>
        </div>
      </div>

      <div className="border border-gray-300 rounded p-4">
        <h2 className="text-lg font-semibold mb-2">AI Analysis</h2>
        {incident.aiAnalysis ? (
          <p className="text-sm text-gray-700">{incident.aiAnalysis}</p>
        ) : (
          <p className="text-sm text-gray-400">AI analysis not available yet.</p>
        )}
      </div>
    </div>
  );
}