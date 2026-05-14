import type {
  OfferList,
  OfferStats,
  Recipe,
  RecipeRequest,
  RefreshResponse,
  Supermarket,
} from "../types";

function resolveApiBase(): string {
  const fromEnv = import.meta.env.VITE_API_URL;
  if (fromEnv) return fromEnv;
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host === "supermarkt-recepten-web.onrender.com") {
      return "https://supermarkt-recepten-api.onrender.com";
    }
  }
  return "";
}

const API_BASE = resolveApiBase();

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      // ignore
    }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

export interface OfferFilters {
  supermarket?: string;
  supermarkets?: string[];
  category?: string;
  q?: string;
  max_price?: number;
  min_discount?: number;
  has_image?: boolean;
  source?: string;
  limit?: number;
  offset?: number;
}

function buildOfferParams(filters: OfferFilters): URLSearchParams {
  const p = new URLSearchParams();
  if (filters.supermarkets && filters.supermarkets.length > 0) {
    p.set("supermarkets", filters.supermarkets.join(","));
  } else if (filters.supermarket) {
    p.set("supermarket", filters.supermarket);
  }
  if (filters.category) p.set("category", filters.category);
  if (filters.q) p.set("q", filters.q);
  if (filters.max_price != null) p.set("max_price", String(filters.max_price));
  if (filters.min_discount != null) p.set("min_discount", String(filters.min_discount));
  if (filters.has_image) p.set("has_image", "true");
  if (filters.source) p.set("source", filters.source);
  if (filters.limit != null) p.set("limit", String(filters.limit));
  if (filters.offset != null) p.set("offset", String(filters.offset));
  return p;
}

export const api = {
  supermarkets: () => request<Supermarket[]>("/api/supermarkets"),
  categories: () => request<string[]>("/api/offers/categories"),
  offers: (filters: OfferFilters = {}) => {
    const qs = buildOfferParams(filters).toString();
    return request<OfferList>(`/api/offers${qs ? `?${qs}` : ""}`);
  },
  offerStats: (filters: OfferFilters = {}) => {
    const qs = buildOfferParams(filters).toString();
    return request<OfferStats>(`/api/offers/stats${qs ? `?${qs}` : ""}`);
  },
  refresh: (supermarket?: string) => {
    const qs = supermarket ? `?supermarket=${encodeURIComponent(supermarket)}` : "";
    return request<RefreshResponse>(`/api/offers/refresh${qs}`, { method: "POST" });
  },
  generateRecipes: (req: RecipeRequest) =>
    request<Recipe[]>("/api/recipes/generate", {
      method: "POST",
      body: JSON.stringify(req),
    }),
  recipesHealth: () => request<{ llm_available: boolean }>("/api/recipes/health"),
};
