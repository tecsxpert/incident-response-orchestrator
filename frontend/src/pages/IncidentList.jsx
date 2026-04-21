import {useEffect, useState} from "react";
import api from "../services/api";

// temporary mock data, will be removed once backend API is ready
const mockIncidents = [
  { id: 1, title: "Database connection timeout", severity: "CRITICAL", status: "OPEN", assignedTo: "Ravi", createdAt: "2026-04-19" },
  { id: 2, title: "API response delay on /orders", severity: "HIGH", status: "IN_PROGRESS", assignedTo: "Priya", createdAt: "2026-04-18" },
  { id: 3, title: "Memory usage above 85%", severity: "MEDIUM", status: "RESOLVED", assignedTo: "Karthik", createdAt: "2026-04-17" },
];

export default function IncidentList() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/incidents")
      .then((res) => {
        setIncidents(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log("Error fetching incidents:", err);
        setIncidents(mockIncidents);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Incidents</h1>
        <div className="space-y-3">
          <div className="h-10 bg-gray-200 rounded animate-pulse mb-2" />
          <div className="h-10 bg-gray-200 rounded animate-pulse mb-2" />
          <div className="h-10 bg-gray-200 rounded animate-pulse mb-2" />
          <div className="h-10 bg-gray-200 rounded animate-pulse mb-2" />
          <div className="h-10 bg-gray-200 rounded animate-pulse mb-2" />
        </div>
      </div>
    );
  }

  if (incidents.length === 0) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Incidents</h1>
        <p className="text-gray-500">No incidents found.</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Incidents</h1>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300 text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="border border-gray-300 px-4 py-2 text-left">ID</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Title</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Severity</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Status</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Assigned To</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Created At</th>
            </tr>
          </thead>
          <tbody>
            {incidents.map((incident) => (
              <tr key={incident.id} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-4 py-2">{incident.id}</td>
                <td className="border border-gray-300 px-4 py-2">{incident.title}</td>
                <td className="border border-gray-300 px-4 py-2">{incident.severity}</td>
                <td className="border border-gray-300 px-4 py-2">{incident.status}</td>
                <td className="border border-gray-300 px-4 py-2">{incident.assignedTo}</td>
                <td className="border border-gray-300 px-4 py-2">{incident.createdAt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}