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

const COLORS = ["#3b82f6", "#f97316", "#22c55e"];

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
    { name: "LOW", count: 8, fill: "#22c55e" },
    { name: "MEDIUM", count: stats.inProgress, fill: "#eab308" },
    { name: "HIGH", count: 12, fill: "#f97316" },
    { name: "CRITICAL", count: stats.open, fill: "#ef4444" },
  ];

  const pieData = [
    { name: "Open", value: stats.open },
    { name: "In Progress", value: stats.inProgress },
    { name: "Resolved", value: stats.resolved },
  ];

  const trendData = mockTrend[period];

  return (
    <div className="p-6 pb-8">
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
          <h2 className="text-lg font-semibold text-gray-700 mb-3">Incidents by Priority</h2>
          <BarChart width={400} height={300} data={barData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" tick={{ fontSize: 13 }} />
            <YAxis tick={{ fontSize: 13 }} />
            <Tooltip />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {barData.map((entry, index) => (
                <Cell key={index} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
       </div>

       <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
         <h2 className="text-lg font-semibold text-gray-700 mb-3">Status Distribution</h2>
          <PieChart width={400} height={300}>
             <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}>
                {pieData.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index]} />
                ))}
            </Pie>
            <Tooltip />
          </PieChart>
       </div>

       <div className="col-span-1 lg:col-span-2 bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
         <h2 className="text-lg font-semibold text-gray-700 mb-3">Incidents Over Time</h2>
         <LineChart width={800} height={300} data={trendData}>
           <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
           <XAxis dataKey="month" tick={{ fontSize: 13 }} />
           <YAxis tick={{ fontSize: 13 }} />
           <Tooltip />
           <Line type="monotone" dataKey="count" stroke="#1B4F8A" strokeWidth={2} />
          </LineChart>
       </div>
     </div>
   </div>
  );
}