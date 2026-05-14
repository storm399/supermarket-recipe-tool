import { useEffect, useMemo, useState } from "react";

import { api } from "../api/client";
import { EmptyState } from "../components/EmptyState";
import { FilterChips } from "../components/FilterChips";
import { LoadingSkeleton } from "../components/LoadingSkeleton";
import { OfferCard } from "../components/OfferCard";
import { StatsPanel } from "../components/StatsPanel";
import { SupermarketFilter } from "../components/SupermarketFilter";
import type { Offer, OfferStats, Supermarket } from "../types";

const PAGE_SIZE = 24;

export default function OffersPage() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [total, setTotal] = useState(0);
  const [stats, setStats] = useState<OfferStats | null>(null);
  const [supermarkets, setSupermarkets] = useState<Supermarket[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedSlugs, setSelectedSlugs] = useState<string[]>([]);
  const [filterCat, setFilterCat] = useState("");
  const [query, setQuery] = useState("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [minDiscount, setMinDiscount] = useState<string>("");
  const [hasImage, setHasImage] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(0);

  useEffect(() => {
    Promise.all([api.supermarkets(), api.categories()])
      .then(([sms, cats]) => {
        setSupermarkets(sms);
        setCategories(cats);
      })
      .catch((e) => setError(String(e.message || e)));
  }, []);

  const filters = useMemo(
    () => ({
      supermarkets: selectedSlugs.length > 0 ? selectedSlugs : undefined,
      category: filterCat || undefined,
      q: query || undefined,
      max_price: maxPrice ? Number(maxPrice) : undefined,
      min_discount: minDiscount ? Number(minDiscount) : undefined,
      has_image: hasImage || undefined,
    }),
    [selectedSlugs, filterCat, query, maxPrice, minDiscount, hasImage]
  );

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      api.offers({ ...filters, limit: PAGE_SIZE, offset: page * PAGE_SIZE }),
      page === 0 ? api.offerStats(filters) : Promise.resolve(stats),
    ])
      .then(([res, st]) => {
        setOffers(res.offers);
        setTotal(res.total);
        if (st) setStats(st);
      })
      .catch((e) => setError(String(e.message || e)))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, page]);

  useEffect(() => {
    setPage(0);
  }, [filters]);

  async function refreshOffers() {
    setRefreshing(true);
    try {
      await api.refresh();
      const res = await api.offers({ limit: PAGE_SIZE });
      setOffers(res.offers);
      setTotal(res.total);
      setPage(0);
      setStats(await api.offerStats());
    } catch (e: any) {
      setError(String(e.message || e));
    } finally {
      setRefreshing(false);
    }
  }

  const chips: { key: string; label: string; onRemove: () => void }[] = [];
  selectedSlugs.forEach((slug) => {
    const sm = supermarkets.find((s) => s.slug === slug);
    chips.push({
      key: `sm-${slug}`,
      label: sm?.name ?? slug,
      onRemove: () => setSelectedSlugs(selectedSlugs.filter((s) => s !== slug)),
    });
  });
  if (filterCat) chips.push({ key: "cat", label: `Categorie: ${filterCat}`, onRemove: () => setFilterCat("") });
  if (query) chips.push({ key: "q", label: `“${query}”`, onRemove: () => setQuery("") });
  if (maxPrice) chips.push({ key: "mp", label: `≤ €${maxPrice}`, onRemove: () => setMaxPrice("") });
  if (minDiscount) chips.push({ key: "md", label: `≥ ${minDiscount}% korting`, onRemove: () => setMinDiscount("") });
  if (hasImage) chips.push({ key: "im", label: "Met afbeelding", onRemove: () => setHasImage(false) });

  function clearAll() {
    setSelectedSlugs([]);
    setFilterCat("");
    setQuery("");
    setMaxPrice("");
    setMinDiscount("");
    setHasImage(false);
  }

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <div className="container">
      <header className="page-head">
        <div>
          <h1>Aanbiedingen</h1>
          <p className="muted">
            Bekijk alle actuele aanbiedingen van 10 supermarkten en filter op wat je nodig hebt.
          </p>
        </div>
        <button onClick={refreshOffers} disabled={refreshing}>
          {refreshing ? "Bezig…" : "Aanbiedingen vernieuwen"}
        </button>
      </header>

      {stats && <StatsPanel stats={stats} supermarkets={supermarkets} activeSlugs={selectedSlugs} />}

      <section className="card filter-card">
        <h2>Filter aanbiedingen</h2>
        <SupermarketFilter
          supermarkets={supermarkets}
          selected={selectedSlugs}
          onChange={setSelectedSlugs}
          counts={stats?.by_supermarket}
        />
        <div className="filters">
          <label>
            Categorie
            <select value={filterCat} onChange={(e) => setFilterCat(e.target.value)}>
              <option value="">Alle categorieën</option>
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </label>
          <label>
            Zoeken
            <input type="text" placeholder="bijv. kip, pasta…" value={query} onChange={(e) => setQuery(e.target.value)} />
          </label>
          <label>
            Max prijs (€)
            <input type="number" min={0} step="0.1" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} placeholder="bv 3.00" />
          </label>
          <label>
            Min korting (%)
            <input type="number" min={0} max={100} value={minDiscount} onChange={(e) => setMinDiscount(e.target.value)} placeholder="bv 20" />
          </label>
          <label className="checkbox-label">
            <input type="checkbox" checked={hasImage} onChange={(e) => setHasImage(e.target.checked)} />
            Alleen met afbeelding
          </label>
        </div>
        <FilterChips chips={chips} onClearAll={chips.length > 0 ? clearAll : undefined} />
      </section>

      {error && <div className="error">Fout: {error}</div>}

      <div className="results-header">
        <span>
          {total} aanbiedingen{selectedSlugs.length > 0 ? " na supermarktfilter" : ""}
          {total > 0 && (
            <span className="muted"> · pagina {page + 1} van {totalPages}</span>
          )}
        </span>
      </div>

      {loading ? (
        <LoadingSkeleton count={6} variant="offer" />
      ) : offers.length === 0 ? (
        <EmptyState
          icon="🛒"
          title="Geen aanbiedingen gevonden"
          message="Pas je filters aan of vernieuw de aanbiedingen."
          actionLabel="Vernieuwen"
          onAction={refreshOffers}
        />
      ) : (
        <>
          <div className="grid offers">
            {offers.map((o) => (
              <OfferCard key={o.id} offer={o} />
            ))}
          </div>
          <div className="pagination">
            <button onClick={() => setPage(Math.max(0, page - 1))} disabled={page === 0}>
              ← Vorige
            </button>
            <span>Pagina {page + 1} van {totalPages}</span>
            <button onClick={() => setPage(page + 1)} disabled={(page + 1) * PAGE_SIZE >= total}>
              Volgende →
            </button>
          </div>
        </>
      )}
    </div>
  );
}
