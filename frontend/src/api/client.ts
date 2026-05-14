import type {
  Offer,
  OfferList,
  Recipe,
  RecipeRequest,
  Supermarket,
} from "../types";

const API_BASE = import.meta.env.VITE_API_URL || "";

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
  category?: string;
  q?: string;
  max_price?: number;
  limit?: number;
  offset?: number;
}

export const api = {
  supermarkets: () => request<Supermarket[]>("/api/supermarkets"),
  categories: () => request<string[]>("/api/offers/categories"),
  offers: (filters: OfferFilters = {}) => {
    const p = new URLSearchParams();
    if (filters.supermarket) p.set("supermarket", filters.supermarket);
    if (filters.category) p.set("category", filters.category);
    if (filters.q) p.set("q", filters.q);
    if (filters.max_price != null) p.set("max_price", String(filters.max_price));
    if (filters.limit != null) p.set("limit", String(filters.limit));
    if (filters.offset != null) p.set("offset", String(filters.offset));
    const qs = p.toString();
    return request<OfferList>(`/api/offers${qs ? `?${qs}` : ""}`);
  },
  offerById: async (id: number): Promise<Offer | null> => {
    const list = await api.offers({ limit: 1000 });
    return list.offers.find((o) => o.id === id) || null;
  },
  refresh: (supermarket?: string) => {
    const qs = supermarket ? `?supermarket=${encodeURIComponent(supermarket)}` : "";
    return request<{ ok: boolean }>(`/api/offers/refresh${qs}`, { method: "POST" });
  },
  generateRecipes: (req: RecipeRequest) =>
    request<Recipe[]>("/api/recipes/generate", {
      method: "POST",
      body: JSON.stringify(req),
    }),
  recipesHealth: () => request<{ llm_available: boolean }>("/api/recipes/health"),
};
