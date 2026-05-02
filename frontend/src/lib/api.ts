// API base URL – reads from env or falls back to localhost
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ── Types ────────────────────────────────────────────────────────────────────

export interface PropertyFeatures {
  location: string;
  size_sqft: number;
  bedrooms: number;
  bathrooms?: number;
  property_type?: "apartment" | "house" | "land" | "commercial" | "studio";
  listing_type?: "sale" | "rent";
  amenities?: string[];
  county?: string;
}

export interface PricePredictionResponse {
  predicted_price_kes: number;
  price_per_sqft_kes: number;
  confidence_interval: { lower: number; upper: number };
  model_version: string;
  disclaimer: string;
}

export interface AvgPriceByBedroom {
  bedrooms: number;
  avg_price_kes: number;
  count: number;
}

export interface NeighborhoodTrend {
  neighborhood: string;
  avg_price_kes: number;
  listing_count: number;
}

// ── API helpers ──────────────────────────────────────────────────────────────

async function fetchJSON<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export async function predictPrice(
  features: PropertyFeatures,
): Promise<PricePredictionResponse> {
  return fetchJSON<PricePredictionResponse>("/predict", {
    method: "POST",
    body: JSON.stringify(features),
  });
}

export async function fetchAvgPriceByBedrooms(
  county?: string,
  listingType?: string,
): Promise<AvgPriceByBedroom[]> {
  const params = new URLSearchParams();
  if (county) params.set("county", county);
  if (listingType) params.set("listing_type", listingType);
  const qs = params.toString() ? `?${params.toString()}` : "";
  return fetchJSON<AvgPriceByBedroom[]>(`/analytics/avg-price-by-bedrooms${qs}`);
}

export async function fetchNeighborhoodTrends(
  county?: string,
  listingType?: string,
  limit = 10,
): Promise<NeighborhoodTrend[]> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (county) params.set("county", county);
  if (listingType) params.set("listing_type", listingType);
  return fetchJSON<NeighborhoodTrend[]>(
    `/analytics/neighborhood-trends?${params.toString()}`,
  );
}

// ── Formatting helpers ───────────────────────────────────────────────────────

export function formatKES(amount: number): string {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency: "KES",
    maximumFractionDigits: 0,
  }).format(amount);
}
