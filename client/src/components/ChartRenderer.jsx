import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { BarChart3 } from "lucide-react";

const COLORS = [
  "#3b82f6", "#8b5cf6", "#06b6d4", "#10b981",
  "#f59e0b", "#ef4444", "#ec4899", "#6366f1",
];

export default function ChartRenderer({ chartType, data, columns }) {
  if (!data.length || chartType === "table" || chartType === "scalar") {
    return null;
  }

  const categoryKey = columns[0];
  const valueKeys = columns.slice(1).filter((col) => {
    const sample = data[0][col];
    return typeof sample === "number" || !isNaN(Number(sample));
  });

  if (!valueKeys.length) return null;

  const chartData = data.slice(0, 20).map((row) => {
    const entry = { [categoryKey]: String(row[categoryKey]) };
    valueKeys.forEach((key) => {
      entry[key] = Number(row[key]) || 0;
    });
    return entry;
  });

  return (
    <div className="rounded-lg border border-gray-700 overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 border-b border-gray-700 text-sm text-gray-400">
        <BarChart3 className="w-4 h-4" />
        Visualization
      </div>
      <div className="p-4 bg-gray-900">
        <ResponsiveContainer width="100%" height={300}>
          {chartType === "bar" ? (
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey={categoryKey} tick={{ fill: "#9ca3af", fontSize: 12 }} />
              <YAxis tick={{ fill: "#9ca3af", fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: "8px" }}
                labelStyle={{ color: "#e5e7eb" }}
              />
              <Legend />
              {valueKeys.map((key, i) => (
                <Bar key={key} dataKey={key} fill={COLORS[i % COLORS.length]} radius={[4, 4, 0, 0]} />
              ))}
            </BarChart>
          ) : chartType === "line" ? (
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey={categoryKey} tick={{ fill: "#9ca3af", fontSize: 12 }} />
              <YAxis tick={{ fill: "#9ca3af", fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: "8px" }}
                labelStyle={{ color: "#e5e7eb" }}
              />
              <Legend />
              {valueKeys.map((key, i) => (
                <Line key={key} type="monotone" dataKey={key} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={{ fill: COLORS[i % COLORS.length] }} />
              ))}
            </LineChart>
          ) : chartType === "pie" ? (
            <PieChart>
              <Pie
                data={chartData}
                dataKey={valueKeys[0]}
                nameKey={categoryKey}
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: "8px" }}
              />
            </PieChart>
          ) : (
            <div />
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
