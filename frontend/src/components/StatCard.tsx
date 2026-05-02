"use client";

import { Building2, Home, MapPin, TrendingUp } from "lucide-react";
import { formatKES } from "@/lib/api";

interface StatCardProps {
  label: string;
  value: string | number;
  sub?: string;
  icon: "home" | "building" | "map" | "trend";
  highlight?: boolean;
}

const ICONS = {
  home: Home,
  building: Building2,
  map: MapPin,
  trend: TrendingUp,
};

export default function StatCard({ label, value, sub, icon, highlight }: StatCardProps) {
  const Icon = ICONS[icon];
  return (
    <div
      className={`rounded-2xl border p-5 shadow-sm ${
        highlight
          ? "border-emerald-200 bg-emerald-50 dark:border-emerald-700 dark:bg-emerald-900/20"
          : "border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-900"
      }`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
            {label}
          </p>
          <p
            className={`mt-1 text-2xl font-bold ${
              highlight ? "text-emerald-700 dark:text-emerald-400" : "text-gray-900 dark:text-white"
            }`}
          >
            {typeof value === "number" ? formatKES(value) : value}
          </p>
          {sub && (
            <p className="mt-1 text-xs text-gray-400 dark:text-gray-500">{sub}</p>
          )}
        </div>
        <span
          className={`rounded-full p-2 ${
            highlight
              ? "bg-emerald-100 text-emerald-600 dark:bg-emerald-800 dark:text-emerald-300"
              : "bg-gray-100 text-gray-500 dark:bg-gray-800 dark:text-gray-400"
          }`}
        >
          <Icon size={20} />
        </span>
      </div>
    </div>
  );
}
