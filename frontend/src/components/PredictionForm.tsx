"use client";

import { useState } from "react";
import {
  type PricePredictionResponse,
  type PropertyFeatures,
  formatKES,
  predictPrice,
} from "@/lib/api";
import { AlertCircle, TrendingUp } from "lucide-react";

const AMENITY_OPTIONS = [
  "parking",
  "gym",
  "swimming pool",
  "borehole",
  "solar",
  "generator",
  "cctv",
  "lift",
  "servant quarters",
  "garden",
  "balcony",
];

export default function PredictionForm() {
  const [form, setForm] = useState<PropertyFeatures>({
    location: "",
    size_sqft: 0,
    bedrooms: 3,
    bathrooms: 2,
    property_type: "apartment",
    listing_type: "sale",
    amenities: [],
    county: "",
  });
  const [result, setResult] = useState<PricePredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function toggleAmenity(amenity: string) {
    setForm((prev) => ({
      ...prev,
      amenities: prev.amenities?.includes(amenity)
        ? prev.amenities.filter((a) => a !== amenity)
        : [...(prev.amenities ?? []), amenity],
    }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.location || form.size_sqft <= 0) {
      setError("Please provide a valid location and size.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await predictPrice(form);
      setResult(res);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "An error occurred.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900">
      <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <TrendingUp size={20} className="text-emerald-600" />
        Price Estimator
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Location */}
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Neighbourhood *
            </span>
            <input
              required
              type="text"
              value={form.location}
              onChange={(e) => setForm({ ...form, location: e.target.value })}
              placeholder="e.g. Kilimani"
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-200
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">County</span>
            <input
              type="text"
              value={form.county ?? ""}
              onChange={(e) => setForm({ ...form, county: e.target.value })}
              placeholder="e.g. Nairobi"
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-200
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            />
          </label>
        </div>

        {/* Size, Bedrooms, Bathrooms */}
        <div className="grid gap-4 sm:grid-cols-3">
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Size (sq ft) *
            </span>
            <input
              required
              type="number"
              min={1}
              value={form.size_sqft || ""}
              onChange={(e) =>
                setForm({ ...form, size_sqft: parseFloat(e.target.value) || 0 })
              }
              placeholder="1200"
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-200
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Bedrooms</span>
            <input
              type="number"
              min={0}
              max={20}
              value={form.bedrooms}
              onChange={(e) => setForm({ ...form, bedrooms: parseInt(e.target.value) || 0 })}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-200
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Bathrooms</span>
            <input
              type="number"
              min={0}
              max={20}
              value={form.bathrooms ?? 1}
              onChange={(e) =>
                setForm({ ...form, bathrooms: parseInt(e.target.value) || 0 })
              }
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-200
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            />
          </label>
        </div>

        {/* Property type & listing type */}
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Property Type
            </span>
            <select
              value={form.property_type}
              onChange={(e) =>
                setForm({
                  ...form,
                  property_type: e.target.value as PropertyFeatures["property_type"],
                })
              }
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            >
              <option value="apartment">Apartment</option>
              <option value="house">House</option>
              <option value="land">Land</option>
              <option value="commercial">Commercial</option>
              <option value="studio">Studio</option>
            </select>
          </label>
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Listing Type
            </span>
            <select
              value={form.listing_type}
              onChange={(e) =>
                setForm({
                  ...form,
                  listing_type: e.target.value as PropertyFeatures["listing_type"],
                })
              }
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm
                         focus:border-emerald-500 focus:outline-none
                         dark:border-gray-600 dark:bg-gray-800 dark:text-white"
            >
              <option value="sale">For Sale</option>
              <option value="rent">For Rent</option>
            </select>
          </label>
        </div>

        {/* Amenities */}
        <div>
          <span className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Amenities
          </span>
          <div className="mt-2 flex flex-wrap gap-2">
            {AMENITY_OPTIONS.map((a) => (
              <button
                key={a}
                type="button"
                onClick={() => toggleAmenity(a)}
                className={`rounded-full border px-3 py-1 text-xs font-medium capitalize transition ${
                  form.amenities?.includes(a)
                    ? "border-emerald-600 bg-emerald-600 text-white"
                    : "border-gray-300 bg-white text-gray-600 hover:border-emerald-400 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300"
                }`}
              >
                {a}
              </button>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="flex items-center gap-2 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-900/30 dark:text-red-400">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-emerald-600 py-2.5 text-sm font-semibold text-white
                     shadow-sm transition hover:bg-emerald-700 focus:outline-none
                     focus:ring-2 focus:ring-emerald-400 disabled:opacity-60"
        >
          {loading ? "Estimating…" : "Estimate Price"}
        </button>
      </form>

      {/* Result */}
      {result && (
        <div className="mt-6 rounded-xl bg-emerald-50 p-5 dark:bg-emerald-900/20">
          <p className="text-xs font-semibold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
            Estimated Price
          </p>
          <p className="mt-1 text-3xl font-bold text-emerald-800 dark:text-emerald-300">
            {formatKES(result.predicted_price_kes)}
          </p>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            {formatKES(result.price_per_sqft_kes)} per sq ft
          </p>
          <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
            95% CI: {formatKES(result.confidence_interval.lower)} –{" "}
            {formatKES(result.confidence_interval.upper)}
          </p>
          <p className="mt-3 text-xs italic text-gray-400">{result.disclaimer}</p>
        </div>
      )}
    </div>
  );
}
