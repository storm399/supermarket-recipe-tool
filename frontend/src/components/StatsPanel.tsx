import type { OfferStats, Supermarket } from "../types";
import { SupermarketLogo } from "./SupermarketLogo";

interface Props {
  stats: OfferStats;
  supermarkets: Supermarket[];
  activeSlugs: string[];
}

export function StatsPanel({ stats, supermarkets, activeSlugs }: Props) {
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
          <span className={`stat-source source-${stats.source}`}>
            {stats.source === "mock" ? "Mockdata" : "Live data"}
          </span>
        </div>
      </div>
      <div className="stats-by-supermarket">
        {supermarkets.map((s) => {
          const count = stats.by_supermarket[s.slug] ?? 0;
          const active = activeSlugs.includes(s.slug);
          return (
            <div key={s.slug} className={`stat-row ${active ? "active" : ""}`}>
              <SupermarketLogo slug={s.slug} name={s.name} size={24} />
              <span className="stat-row-count">{count}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
