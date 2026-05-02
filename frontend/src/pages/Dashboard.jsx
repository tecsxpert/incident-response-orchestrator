import {useEffect, useState} from "react";
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip} from "recharts";
import api from "../services/api";

const mockStats = {
  total: 50,
  open: 20,
  inProgress: 15,
  resolved: 15,
};

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/incidents/stats")
      .then((res) => {
        setStats(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log("Error fetching stats:", err);
        setStats(mockStats);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="h-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-24 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>
    );
  }

  if (!stats || stats.total === 0) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
        <div className="text-center py-16">
          <p className="text-gray-400 text-lg">No incidents to display yet.</p>
          <p className="text-gray-300 text-sm mt-1">Create your first incident to see stats here.</p>
        </div>
      </div>
    );
  }

  const chartData = [
    {name: "Open", count: stats.open},
    {name: "In Progress", count: stats.inProgress},
    {name: "Resolved", count: stats.resolved},
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="border border-gray-300 rounded p-4">
          <p className="text-sm text-gray-500">Total</p>
          <p className="text-3xl font-bold">{stats.total}</p>
        </div>
        <div className="border border-gray-300 rounded p-4">
          <p className="text-sm text-gray-500">Open</p>
          <p className="text-3xl font-bold">{stats.open}</p>
        </div>
        <div className="border border-gray-300 rounded p-4">
          <p className="text-sm text-gray-500">In Progress</p>
          <p className="text-3xl font-bold">{stats.inProgress}</p>
        </div>
        <div className="border border-gray-300 rounded p-4">
          <p className="text-sm text-gray-500">Resolved</p>
          <p className="text-3xl font-bold">{stats.resolved}</p>
        </div>
      </div>

      <h2 className="text-lg font-semibold mb-3">Incidents by Status</h2>
      <BarChart width={500} height={300} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="#7c3aed" />
      </BarChart>
    </div>
  );
}