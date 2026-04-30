import {useEffect, useState, useCallback} from "react";
import {useNavigate, useSearchParams} from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import api from "../services/api";

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

    let url = `/api/incidents/all?page=${page}&size=10&sort=${sortField},${sortDir}`;
    if (debounced) url = `/api/incidents/search?q=${debounced}&page=${page}&size=10`;
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

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Incidents</h1>
        <button
          onClick={() => navigate("/create")}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm">
          Create Incident
        </button>
      </div>

      <div className="flex gap-3 mb-4 flex-wrap">
        <input
          type="text"
          placeholder="Search incidents..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2 text-sm w-64" />
        <select
          value={status}
          onChange={(e) => { setStatus(e.target.value); setPage(0); }}
          className="border border-gray-300 rounded px-3 py-2 text-sm">
          <option value="">All Status</option>
          <option value="OPEN">OPEN</option>
          <option value="IN_PROGRESS">IN_PROGRESS</option>
          <option value="RESOLVED">RESOLVED</option>
        </select>
        <DatePicker
          selected={fromDate}
          onChange={(date) => { setFromDate(date); setPage(0); }}
          placeholderText="From date"
          className="border border-gray-300 rounded px-3 py-2 text-sm" />
        <DatePicker
          selected={toDate}
          onChange={(date) => { setToDate(date); setPage(0); }}
          placeholderText="To date"
          className="border border-gray-300 rounded px-3 py-2 text-sm" />
      </div>

      {incidents.length === 0 ? (
        <p className="text-gray-500">No incidents found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300 text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border border-gray-300 px-4 py-2 text-left">ID</th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("title")}>
                  Title {sortField === "title" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("priority")}>
                  Priority {sortField === "priority" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("status")}>
                  Status {sortField === "status" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th className="border border-gray-300 px-4 py-2 text-left">Assigned To</th>
                <th
                  className="border border-gray-300 px-4 py-2 text-left cursor-pointer"
                  onClick={() => handleSort("createdAt")}>
                  Created At {sortField === "createdAt" ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
                <th className="border border-gray-300 px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {incidents.map((incident) => (
                <tr key={incident.id} className="hover:bg-gray-50">
                  <td className="border border-gray-300 px-4 py-2">{incident.id}</td>
                  <td
                    className="border border-gray-300 px-4 py-2 cursor-pointer text-blue-600 hover:underline"
                    onClick={() => navigate(`/incidents/${incident.id}`)}>
                    {incident.title}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">{incident.priority}</td>
                  <td className="border border-gray-300 px-4 py-2">{incident.status}</td>
                  <td className="border border-gray-300 px-4 py-2">{incident.assignedTo}</td>
                  <td className="border border-gray-300 px-4 py-2">{incident.createdAt}</td>
                  <td className="border border-gray-300 px-4 py-2">
                    <button
                      onClick={() => navigate(`/edit/${incident.id}`)}
                      className="text-blue-600 hover:underline text-xs">
                      Edit
                    </button>
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
          className="px-3 py-1 border rounded text-sm disabled:opacity-50">
          Previous
        </button>
        <span className="text-sm">Page {page + 1} of {totalPages}</span>
        <button
          onClick={() => setPage(page + 1)}
          disabled={page + 1 >= totalPages}
          className="px-3 py-1 border rounded text-sm disabled:opacity-50">
          Next
        </button>
      </div>
    </div>
  );
}