import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";
import { SupermarketLogo } from "../components/SupermarketLogo";
import type { OfferStats, Supermarket } from "../types";

export default function HomePage() {
  const [stats, setStats] = useState<OfferStats | null>(null);
  const [supermarkets, setSupermarkets] = useState<Supermarket[]>([]);

  useEffect(() => {
    api.offerStats().then(setStats).catch(() => setStats(null));
    api.supermarkets().then(setSupermarkets).catch(() => setSupermarkets([]));
  }, []);

  return (
    <div className="home">
      <section className="hero">
        <div className="hero-inner">
          <span className="hero-eyebrow">🥦 Slim koken met aanbiedingen</span>
          <h1 className="hero-title">
            Kies je supermarkt, <span className="accent">bespaar direct</span>
            <br /> en kook gezond.
          </h1>
          <p className="hero-lead">
            Geen zin om naar vijf winkels te gaan? Wij combineren actuele aanbiedingen
            tot complete recepten — gezond, betaalbaar en makkelijk te koken.
          </p>
          <div className="hero-badges">
            <span className="hero-badge">💸 Bespaar geld</span>
            <span className="hero-badge">🥗 Eet gezonder</span>
            <span className="hero-badge">♻️ Minder verspilling</span>
            <span className="hero-badge">⏱️ Klaar in een half uur</span>
          </div>
          <div className="hero-cta">
            <Link to="/recepten" className="btn primary">Genereer recepten</Link>
            <Link to="/aanbiedingen" className="btn ghost">Bekijk aanbiedingen</Link>
          </div>
          {stats && (
            <div className="hero-stats">
              <div><b>{stats.total}</b><small>aanbiedingen</small></div>
              <div><b>{Object.keys(stats.by_supermarket).length}</b><small>supermarkten</small></div>
              {stats.average_discount_percent != null && (
                <div><b>{stats.average_discount_percent}%</b><small>gem. korting</small></div>
              )}
            </div>
          )}
        </div>
      </section>

      <section className="home-section">
        <h2>Ondersteunde supermarkten</h2>
        <p className="muted">10 Nederlandse supermarkten — kies één voor recepten uit één winkel.</p>
        <div className="supermarket-grid">
          {supermarkets.map((s) => (
            <div className="supermarket-tile" key={s.slug}>
              <SupermarketLogo slug={s.slug} name={s.name} size={42} />
              <span>{s.name}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="home-section how-it-works">
        <h2>Zo werkt het</h2>
        <div className="steps">
          <div className="step">
            <span className="step-num">1</span>
            <h3>Kies je supermarkt</h3>
            <p>Selecteer 1 of meer favoriete supermarkten. Wij filteren de rest weg.</p>
          </div>
          <div className="step">
            <span className="step-num">2</span>
            <h3>Stel je voorkeuren in</h3>
            <p>Vegetarisch, max prep-tijd, budget per portie of min eiwit — alles is mogelijk.</p>
          </div>
          <div className="step">
            <span className="step-num">3</span>
            <h3>Krijg 12+ recepten</h3>
            <p>Compleet met ingrediënten, stappen, voedingswaarden en gezondheidsscore.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
