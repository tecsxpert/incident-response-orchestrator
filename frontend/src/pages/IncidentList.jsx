import {useEffect, useState, useCallback} from "react";
import {useNavigate, useSearchParams} from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import api from "../services/api";

const priorityColors = {
  LOW: "bg-green-100 text-green-700",
  MEDIUM: "bg-yellow-100 text-yellow-700",
  HIGH: "bg-orange-100 text-orange-700",
  CRITICAL: "bg-red-100 text-red-700",
};

const statusColors = {
  OPEN: "bg-blue-100 text-blue-700",
  IN_PROGRESS: "bg-orange-100 text-orange-700",
  RESOLVED: "bg-green-100 text-green-700",
};

// temporary mock data, will be removed once backend API is ready
const mockIncidents = [
  { id: 1, title: "Database connection timeout", priority: "CRITICAL", status: "OPEN", assignedTo: "Ravi", createdAt: "2026-04-15" },
  { id: 2, title: "API response delay on /orders", priority: "HIGH", status: "IN_PROGRESS", assignedTo: "Priya", createdAt: "2026-04-14" },
  { id: 3, title: "Memory usage above 85%", priority: "MEDIUM", status: "RESOLVED", assignedTo: "Karthik", createdAt: "2026-04-13" },
];

export default function IncidentList() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [sortField, setSortField] = useState("createdAt");
  const [sortDir, setSortDir] = useState("desc");

  const [search, setSearch] = useState(searchParams.get("q") || "");
  const [status, setStatus] = useState(searchParams.get("status") || "");
  const [fromDate, setFromDate] = useState(null);
  const [toDate, setToDate] = useState(null);
  const [debounced, setDebounced] = useState(search);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebounced(search);
      setPage(0);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    const params = {};
    if (debounced) params.q = debounced;
    if (status) params.status = status;
    setSearchParams(params);
  }, [debounced, status]);

  const fetchIncidents = useCallback(() => {
    setLoading(true);
    const from = fromDate ? fromDate.toISOString().split("T")[0] : "";
    const to = toDate ? toDate.toISOString().split("T")[0] : "";

    let url = `/incidents?page=${page}&size=10&sortBy=${sortField}&sortDir=${sortDir}`;
    if (debounced) url = `/incidents?q=${debounced}&page=${page}&size=10&sortBy=${sortField}&sortDir=${sortDir}`;
    if (status) url += `&status=${status}`;
    if (from) url += `&from=${from}`;
    if (to) url += `&to=${to}`;

    api.get(url)
      .then((res) => {
        setIncidents(res.data.content || res.data);
        setTotalPages(res.data.totalPages || 1);
        setLoading(false);
      })
      .catch((err) => {
        console.log("Error fetching incidents:", err);
        setIncidents(mockIncidents);
        setTotalPages(1);
        setLoading(false);
      });
  }, [page, sortField, sortDir, debounced, status, fromDate, toDate]);

  useEffect(() => {
    fetchIncidents();
  }, [fetchIncidents]);

  function handleSort(field) {
    if (sortField === field) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDir("asc");
    }
  }

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

  function handleExport() {
    window.open(`${import.meta.env.VITE_API_URL}/api/incidents/export`, "_blank");
  }

  return (
    <div className="p-6">
      <div className="flex flex-wrap justify-between items-center mb-4 gap-2">
        <h1 className="text-2xl font-bold">Incidents</h1>
        <div className="flex gap-2">
        <button
          onClick={handleExport}
          className="border border-gray-300 hover:bg-gray-100 px-2 py-1 sm:px-4 sm:py-2 rounded text-xs sm:text-sm"> 
          Export CSV
        </button>
        <button
          onClick={() => navigate("/create")}
          className="bg-brand hover:bg-blue-900 bg-brand text-white px-2 py-1 sm:px-4 sm:py-2 rounded text-xs sm:text-sm">
          Create Incident
        </button>
      </div>
    </div>

      <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm mb-4 flex gap-2 flex-wrap items-center hover:shadow-md transition-shadow">
        <input
          type="text"
          placeholder="Search incidents..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 text-sm w-36" />
        <select
          value={status}
          onChange={(e) => { setStatus(e.target.value); setPage(0); }}
          className="border border-gray-300 rounded px-3 py-2 text-sm">
          <option value="">All Status</option>
          <option value="OPEN">OPEN</option>
          <option value="IN_PROGRESS">IN_PROGRESS</option>
          <option value="RESOLVED">RESOLVED</option>
        </select>
        <div className="flex gap-2">
          <DatePicker
            selected={fromDate}
            onChange={(date) => { setFromDate(date); setPage(0); }}
            placeholderText="From date"
            className="border border-gray-300 rounded px-3 py-2 text-sm w-28" />
          <DatePicker
            selected={toDate}
            onChange={(date) => { setToDate(date); setPage(0); }}
            placeholderText="To date"
            className="border border-gray-300 rounded px-3 py-2 text-sm w-28" />
        </div>
      </div>

      {incidents.length === 0 ? (
        <p className="text-gray-500">No incidents found.</p>
      ) : (
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300 text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors">ID</th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors"
                  onClick={() => handleSort("title")}>
                  Title {sortField === "title" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors"
                  onClick={() => handleSort("priority")}>
                  Priority {sortField === "priority" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors"
                  onClick={() => handleSort("status")}>
                  Status {sortField === "status" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors">Assigned To</th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors"
                  onClick={() => handleSort("createdAt")}>
                  Created At {sortField === "createdAt" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th className="border border-gray-300 px-4 py-2 text-left cursor-pointer hover:bg-gray-200 transition-colors">Actions</th>
              </tr>
            </thead>
            <tbody>
              {incidents.map((incident) => (
                <tr key={incident.id} className="hover:bg-blue-50 transition-colors">
                  <td className="border border-gray-300 px-4 py-2">{incident.id}</td>
                  <td
                    className="border border-gray-300 px-4 py-2 cursor-pointer text-brand hover:underline"
                    onClick={() => navigate(`/incidents/${incident.id}`)}>
                    {incident.title}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${priorityColors[incident.priority]}`}>
                      {incident.priority}
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[incident.status]}`}>
                      {incident.status}
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-2">{incident.assignedTo}</td>
                  <td className="border border-gray-300 px-4 py-2">{incident.createdAt}</td>
                  <td className="border border-gray-300 px-4 py-2">
                    <div className="flex gap-2">
                      <button
                        onClick={() => navigate(`/incidents/${incident.id}`)}
                        className="text-brand hover:underline text-xs">
                        View
                      </button>
                      <button
                        onClick={() => navigate(`/edit/${incident.id}`)}
                        className="text-blue-600 hover:underline text-xs">
                        Edit
                      </button>
                   </div>
                 </td>
               </tr>
             ))}
           </tbody>
          </table>
        </div>
      )}

      <div className="flex gap-2 mt-4 items-center">
        <button
          onClick={() => setPage(page - 1)}
          disabled={page === 0}
          className="px-3 py-1 border rounded text-sm disabled:opacity-50 hover:bg-gray-100 transition-colors">
          Previous
        </button>
        <span className="text-sm">Page {page + 1} of {totalPages}</span>
        <button
          onClick={() => setPage(page + 1)}
          disabled={page + 1 >= totalPages}
          className="px-3 py-1 border rounded text-sm disabled:opacity-50 hover:bg-gray-100 transition-colors">
          Next
        </button>
      </div>
    </div>
  );
}