"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { type AvgPriceByBedroom, formatKES } from "@/lib/api";

interface AvgPriceChartProps {
  data: AvgPriceByBedroom[];
}

function CustomTooltip({ active, payload, label }: {
  active?: boolean;
  payload?: Array<{ value: number }>;
  label?: string | number;
}) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-lg dark:border-gray-700 dark:bg-gray-900">
      <p className="text-sm font-semibold text-gray-700 dark:text-gray-300">
        {label === 0 ? "Studio" : `${label} Bedroom${Number(label) !== 1 ? "s" : ""}`}
      </p>
      <p className="text-emerald-600 dark:text-emerald-400">
        Avg: {formatKES(payload[0].value)}
      </p>
    </div>
  );
}

export default function AvgPriceChart({ data }: AvgPriceChartProps) {
  if (!data.length) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-gray-400">
        No data available
      </div>
    );
  }

  const chartData = data.map((d) => ({
    name: d.bedrooms === 0 ? "Studio" : `${d.bedrooms} Bed`,
    avg_price: d.avg_price_kes,
    count: d.count,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis
          dataKey="name"
          tick={{ fontSize: 12, fill: "#6b7280" }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tickFormatter={(v: number) =>
            v >= 1_000_000 ? `${(v / 1_000_000).toFixed(1)}M` : `${(v / 1_000).toFixed(0)}K`
          }
          tick={{ fontSize: 11, fill: "#6b7280" }}
          axisLine={false}
          tickLine={false}
          width={55}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: "#d1fae5" }} />
        <Bar dataKey="avg_price" fill="#059669" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
