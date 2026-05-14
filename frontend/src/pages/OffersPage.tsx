import { useEffect, useMemo, useState } from "react";

import { api } from "../api/client";
import { OfferCard } from "../components/OfferCard";
import type { Offer, Supermarket } from "../types";

export default function OffersPage() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [total, setTotal] = useState(0);
  const [supermarkets, setSupermarkets] = useState<Supermarket[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [filterSm, setFilterSm] = useState("");
  const [filterCat, setFilterCat] = useState("");
  const [query, setQuery] = useState("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    Promise.all([api.supermarkets(), api.categories()])
      .then(([sms, cats]) => {
        setSupermarkets(sms);
        setCategories(cats);
      })
      .catch((e) => setError(String(e.message || e)));
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    api
      .offers({
        supermarket: filterSm || undefined,
        category: filterCat || undefined,
        q: query || undefined,
        max_price: maxPrice ? Number(maxPrice) : undefined,
        limit: 200,
      })
      .then((res) => {
        setOffers(res.offers);
        setTotal(res.total);
      })
      .catch((e) => setError(String(e.message || e)))
      .finally(() => setLoading(false));
  }, [filterSm, filterCat, query, maxPrice]);

  async function refreshOffers() {
    setRefreshing(true);
    try {
      await api.refresh();
      const res = await api.offers({ limit: 200 });
      setOffers(res.offers);
      setTotal(res.total);
    } catch (e: any) {
      setError(String(e.message || e));
    } finally {
      setRefreshing(false);
    }
  }

  const showing = useMemo(() => offers.length, [offers]);

  return (
    <div className="container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "0.5rem" }}>
        <h1>Actuele aanbiedingen</h1>
        <button onClick={refreshOffers} disabled={refreshing}>
          {refreshing ? "Bezig met ophalen…" : "Aanbiedingen vernieuwen"}
        </button>
      </div>
      <p className="muted">
        {total > 0 ? `${showing} van ${total} aanbiedingen getoond.` : "Nog geen aanbiedingen geladen."}
      </p>

      <div className="filters">
        <label>
          Supermarkt
          <select value={filterSm} onChange={(e) => setFilterSm(e.target.value)}>
            <option value="">Alle supermarkten</option>
            {supermarkets.map((s) => (
              <option key={s.slug} value={s.slug}>{s.name}</option>
            ))}
          </select>
        </label>
        <label>
          Categorie
          <select value={filterCat} onChange={(e) => setFilterCat(e.target.value)}>
            <option value="">Alle categorieen</option>
            {categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
        <label>
          Zoeken
          <input
            type="text"
            placeholder="bijv. kip, pasta…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <label>
          Max prijs (€)
          <input
            type="number"
            min={0}
            step="0.1"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="bijv. 3.00"
          />
        </label>
      </div>

      {error && <div className="error">Fout: {error}</div>}
      {loading ? (
        <div className="loading">Aanbiedingen laden…</div>
      ) : offers.length === 0 ? (
        <div className="empty">Geen aanbiedingen gevonden met deze filters.</div>
      ) : (
        <div className="grid offers">
          {offers.map((o) => (
            <OfferCard key={o.id} offer={o} />
          ))}
        </div>
      )}
    </div>
  );
}
