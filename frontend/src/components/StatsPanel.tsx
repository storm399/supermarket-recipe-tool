import { useState } from "react";
import { api } from "../api/client";
import type { OfferStats, ScrapeResult, Supermarket } from "../types";
import { SourceBadge } from "./SourceBadge";
import { SupermarketLogo } from "./SupermarketLogo";

interface Props {
  stats: OfferStats;
  supermarkets: Supermarket[];
  activeSlugs: string[];
  onRefreshed?: () => void;
}

export function StatsPanel({ stats, supermarkets, activeSlugs, onRefreshed }: Props) {
  const [busySlug, setBusySlug] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, ScrapeResult>>({});

  async function refreshOne(slug: string) {
    setBusySlug(slug);
    try {
      const res = await api.refresh(slug);
      const r = res.results[0];
      if (r) setResults((prev) => ({ ...prev, [slug]: r }));
      onRefreshed?.();
    } catch (e: any) {
      setResults((prev) => ({
        ...prev,
        [slug]: {
          supermarket: slug,
          source: "fallback_mock",
          fetched: 0,
          saved: 0,
          duplicates_skipped: 0,
          ok: false,
          error: String(e.message || e),
          duration_ms: 0,
        },
      }));
    } finally {
      setBusySlug(null);
    }
  }

  return (
    <section className="stats-panel">
      <div className="stats-summary">
        <div className="stat">
          <span className="stat-value">{stats.total}</span>
          <span className="stat-label">aanbiedingen{activeSlugs.length ? " (na filter)" : ""}</span>
        </div>
        {stats.average_discount_percent != null && (
          <div className="stat">
            <span className="stat-value">{stats.average_discount_percent}%</span>
            <span className="stat-label">gemiddelde korting</span>
          </div>
        )}
        <div className="stat">
          <span className="stat-value">{Object.keys(stats.by_supermarket).length}</span>
          <span className="stat-label">supermarkten actief</span>
        </div>
        <div className="stat">
          <SourceBadge source={stats.source} />
        </div>
      </div>
      <div className="stats-by-supermarket">
        {supermarkets.map((s) => {
          const count = stats.by_supermarket[s.slug] ?? 0;
          const active = activeSlugs.includes(s.slug);
          const result = results[s.slug];
          return (
            <div key={s.slug} className={`stat-row ${active ? "active" : ""}`}>
              <SupermarketLogo slug={s.slug} name={s.name} size={22} />
              <span className="stat-row-count">{count}</span>
              <button
                type="button"
                className="stat-row-refresh"
                title={`Vernieuw ${s.name}`}
                onClick={() => refreshOne(s.slug)}
                disabled={busySlug === s.slug}
              >
                {busySlug === s.slug ? "⏳" : "🔄"}
              </button>
              {result && (
                <span
                  className={`stat-row-result ${result.ok ? "ok" : "fail"}`}
                  title={result.error || `${result.fetched} opgehaald, ${result.saved} opgeslagen`}
                >
                  {result.ok ? `+${result.saved}` : "✗"}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
