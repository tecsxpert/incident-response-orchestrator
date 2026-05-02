import {useEffect, useState} from "react";
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, LineChart, Line} from "recharts";
import api from "../services/api";

const mockStats = {
  total: 50,
  open: 20,
  inProgress: 15,
  resolved: 15,
};

const mockTrend = {
  1: [
    { month: "Nov", count: 5 },
    { month: "Dec", count: 8 },
    { month: "Jan", count: 6 },
    { month: "Feb", count: 10 },
    { month: "Mar", count: 7 },
    { month: "Apr", count: 12 },
  ],
  3: [
    { month: "Feb", count: 10 },
    { month: "Mar", count: 7 },
    { month: "Apr", count: 12 },
  ],
  6: [
    { month: "Nov", count: 5 },
    { month: "Dec", count: 8 },
    { month: "Jan", count: 6 },
    { month: "Feb", count: 10 },
    { month: "Mar", count: 7 },
    { month: "Apr", count: 12 },
  ],
};

const COLORS = ["#3b82f6", "#a855f7", "#22c55e"];

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState(6);

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
        <h1 className="text-2xl font-bold mb-4">Analytics</h1>
        <div className="h-64 bg-gray-200 rounded animate-pulse" />
      </div>
    );
  }

  if (!stats || stats.total === 0) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Analytics</h1>
        <div className="text-center py-16">
          <p className="text-gray-400 text-lg">No data available yet.</p>
          <p className="text-gray-300 text-sm mt-1">Incidents will appear here once created.</p>
        </div>
      </div>
   );
 }

  const barData = [
    { name: "LOW", count: 8 },
    { name: "MEDIUM", count: stats.inProgress },
    { name: "HIGH", count: 12 },
    { name: "CRITICAL", count: stats.open },
  ];

  const pieData = [
    { name: "Open", value: stats.open },
    { name: "In Progress", value: stats.inProgress },
    { name: "Resolved", value: stats.resolved },
  ];

  const trendData = mockTrend[period];

  return (
    <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold mb-6">Analytics</h1>
          <select
            value={period}
            onChange={(e) => setPeriod(Number(e.target.value))}
            className="border border-gray-300 rounded px-3 py-2 text-sm">
            <option value={1}>Last 1 month</option>
            <option value={3}>Last 3 months</option>
            <option value={6}>Last 6 months</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-8">
        <div>
          <h2 className="text-lg font-semibold mb-3">Incidents by Status</h2>
          <BarChart width={400} height={300} data={barData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#7c3aed" />
          </BarChart>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-3">Status Distribution</h2>
          <PieChart width={400} height={300}>
            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label>
              {pieData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>

        <div className="col-span-2">
          <h2 className="text-lg font-semibold mb-3">Incidents Over Time</h2>
          <LineChart width={800} height={300} data={trendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" stroke="#7c3aed" />
          </LineChart>
        </div>
      </div>
    </div>
  );
}