import {useEffect, useState} from "react";
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip} from "recharts";
import api from "../services/api";
import {AlertCircle, Clock, CheckCircle, BarChart2} from "lucide-react";

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
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-sm text-gray-400 mt-1">Overview of all incidents</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="border border-gray-200 rounded-xl p-5 shadow-sm bg-white hover:shadow-md transition-shadow">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500 mb-1">Total Incidents</p>
              <p className="text-3xl font-bold text-brand">{stats.total}</p>
            </div>
            <BarChart2 className="text-brand opacity-60" size={24} />
          </div>
        </div>
        <div className="border border-gray-200 rounded-xl p-5 shadow-sm bg-white hover:shadow-md transition-shadow">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500 mb-1">Open</p>
              <p className="text-3xl font-bold text-blue-500">{stats.open}</p>
            </div>
            <AlertCircle className="text-blue-500 opacity-60" size={24} />
          </div>
        </div>
        <div className="border border-gray-200 rounded-xl p-5 shadow-sm bg-white hover:shadow-md transition-shadow">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500 mb-1">In Progress</p>
              <p className="text-3xl font-bold text-yellow-500">{stats.inProgress}</p>
            </div>
            <Clock className="text-yellow-500 opacity-60" size={24} />
          </div>
        </div>
        <div className="border border-gray-200 rounded-xl p-5 shadow-sm bg-white hover:shadow-md transition-shadow">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500 mb-1">Resolved</p>
              <p className="text-3xl font-bold text-green-500">{stats.resolved}</p>
            </div>
            <CheckCircle className="text-green-500 opacity-60" size={24} />
          </div>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
        <h2 className="text-lg font-semibold text-gray-700 mb-4">Incidents by Status</h2>
        <BarChart width={600} height={300} data={chartData} margin={{ left: -20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="name" tick={{ fontSize: 13 }} />
          <YAxis tick={{ fontSize: 13 }} />
          <Tooltip />
          <Bar dataKey="count" fill="#1B4F8A" radius={[4, 4, 0, 0]} />
        </BarChart>
      </div>
    </div>
  );
}