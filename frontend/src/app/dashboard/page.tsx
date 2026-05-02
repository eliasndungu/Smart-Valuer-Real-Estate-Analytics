"use client";

import { useEffect, useState } from "react";
import AvgPriceChart from "@/components/AvgPriceChart";
import NeighborhoodChart from "@/components/NeighborhoodChart";
import StatCard from "@/components/StatCard";
import {
  type AvgPriceByBedroom,
  type NeighborhoodTrend,
  fetchAvgPriceByBedrooms,
  fetchNeighborhoodTrends,
  formatKES,
} from "@/lib/api";

// ── Fallback mock data (shown when the API is unavailable) ──────────────────

const MOCK_AVG_BY_BEDROOMS: AvgPriceByBedroom[] = [
  { bedrooms: 0, avg_price_kes: 2_800_000, count: 45 },
  { bedrooms: 1, avg_price_kes: 5_500_000, count: 120 },
  { bedrooms: 2, avg_price_kes: 9_200_000, count: 210 },
  { bedrooms: 3, avg_price_kes: 15_400_000, count: 380 },
  { bedrooms: 4, avg_price_kes: 24_000_000, count: 150 },
  { bedrooms: 5, avg_price_kes: 38_000_000, count: 60 },
];

const MOCK_NEIGHBORHOOD_TRENDS: NeighborhoodTrend[] = [
  { neighborhood: "Karen", avg_price_kes: 45_000_000, listing_count: 85 },
  { neighborhood: "Runda", avg_price_kes: 52_000_000, listing_count: 62 },
  { neighborhood: "Muthaiga", avg_price_kes: 60_000_000, listing_count: 48 },
  { neighborhood: "Lavington", avg_price_kes: 32_000_000, listing_count: 110 },
  { neighborhood: "Kilimani", avg_price_kes: 18_000_000, listing_count: 220 },
  { neighborhood: "Westlands", avg_price_kes: 16_500_000, listing_count: 195 },
  { neighborhood: "Kileleshwa", avg_price_kes: 15_000_000, listing_count: 175 },
  { neighborhood: "Parklands", avg_price_kes: 14_000_000, listing_count: 160 },
  { neighborhood: "South B", avg_price_kes: 9_500_000, listing_count: 140 },
  { neighborhood: "Embakasi", avg_price_kes: 7_200_000, listing_count: 200 },
];

// ── Dashboard component ─────────────────────────────────────────────────────

export default function DashboardPage() {
  const [avgByBedrooms, setAvgByBedrooms] = useState<AvgPriceByBedroom[]>([]);
  const [trends, setTrends] = useState<NeighborhoodTrend[]>([]);
  const [loading, setLoading] = useState(true);
  const [usingMockData, setUsingMockData] = useState(false);
  const [county, setCounty] = useState("");
  const [listingType, setListingType] = useState("");

  async function loadData() {
    setLoading(true);
    try {
      const [beds, hoods] = await Promise.all([
        fetchAvgPriceByBedrooms(county || undefined, listingType || undefined),
        fetchNeighborhoodTrends(county || undefined, listingType || undefined),
      ]);
      setAvgByBedrooms(beds.length ? beds : MOCK_AVG_BY_BEDROOMS);
      setTrends(hoods.length ? hoods : MOCK_NEIGHBORHOOD_TRENDS);
      setUsingMockData(beds.length === 0 && hoods.length === 0);
    } catch {
      // API unreachable – use mock data
      setAvgByBedrooms(MOCK_AVG_BY_BEDROOMS);
      setTrends(MOCK_NEIGHBORHOOD_TRENDS);
      setUsingMockData(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [county, listingType]);

  // Summary stats derived from data
  const totalListings = trends.reduce((s, t) => s + t.listing_count, 0);
  const overallAvg =
    avgByBedrooms.length
      ? avgByBedrooms.reduce((s, d) => s + d.avg_price_kes * d.count, 0) /
        avgByBedrooms.reduce((s, d) => s + d.count, 0)
      : 0;
  const topNeighborhood = trends[0]?.neighborhood ?? "—";

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Market Dashboard
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Kenyan real estate analytics · {usingMockData ? "Sample data" : "Live data"}
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <select
            value={county}
            onChange={(e) => setCounty(e.target.value)}
            className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm
                       focus:border-emerald-500 focus:outline-none
                       dark:border-gray-600 dark:bg-gray-800 dark:text-white"
          >
            <option value="">All Counties</option>
            <option value="Nairobi">Nairobi</option>
            <option value="Mombasa">Mombasa</option>
            <option value="Kisumu">Kisumu</option>
            <option value="Nakuru">Nakuru</option>
            <option value="Kiambu">Kiambu</option>
          </select>
          <select
            value={listingType}
            onChange={(e) => setListingType(e.target.value)}
            className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm
                       focus:border-emerald-500 focus:outline-none
                       dark:border-gray-600 dark:bg-gray-800 dark:text-white"
          >
            <option value="">Sale &amp; Rent</option>
            <option value="sale">For Sale</option>
            <option value="rent">For Rent</option>
          </select>
        </div>
      </div>

      {/* Stat cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="Total Listings"
          value={totalListings.toLocaleString()}
          icon="building"
        />
        <StatCard
          label="Overall Avg Price"
          value={overallAvg}
          sub="across all bedroom types"
          icon="trend"
          highlight
        />
        <StatCard
          label="Top Neighbourhood"
          value={topNeighborhood}
          sub="by listing volume"
          icon="map"
        />
        <StatCard
          label="Avg Price / sq ft"
          value={
            overallAvg && avgByBedrooms[2]
              ? formatKES(overallAvg / 1200) + " est."
              : "—"
          }
          icon="home"
        />
      </div>

      {/* Charts */}
      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-emerald-200 border-t-emerald-600" />
        </div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Average Price per Bedroom */}
          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900">
            <h2 className="mb-1 text-base font-semibold text-gray-900 dark:text-white">
              Average Price per Bedroom
            </h2>
            <p className="mb-4 text-xs text-gray-500 dark:text-gray-400">
              Mean listing price (KES) grouped by bedroom count
            </p>
            <AvgPriceChart data={avgByBedrooms} />
          </div>

          {/* Neighbourhood Trends */}
          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900">
            <h2 className="mb-1 text-base font-semibold text-gray-900 dark:text-white">
              Neighbourhood Trends
            </h2>
            <p className="mb-4 text-xs text-gray-500 dark:text-gray-400">
              Average price by neighbourhood (top 10 by listing volume)
            </p>
            <NeighborhoodChart data={trends} />
          </div>
        </div>
      )}

      {usingMockData && (
        <p className="text-center text-xs text-amber-600 dark:text-amber-400">
          ⚠️ Showing sample data. Connect the FastAPI backend to see live analytics.
        </p>
      )}
    </div>
  );
}
