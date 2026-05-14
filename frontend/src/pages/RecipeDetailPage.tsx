import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { HealthScoreBadge } from "../components/HealthScoreBadge";
import { RecipeImage } from "../components/RecipeImage";
import { SupermarketLogo } from "../components/SupermarketLogo";
import type { Recipe } from "../types";

const WARN_LABELS = new Set(["veel zout", "veel suiker"]);
const MEAL_LABELS: Record<string, string> = {
  ontbijt: "Ontbijt",
  lunch: "Lunch",
  diner: "Diner",
  snack: "Snack",
  "meal-prep": "Meal prep",
};

export default function RecipeDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [recipe, setRecipe] = useState<Recipe | null>(null);

  useEffect(() => {
    if (!id) return;
    const raw = sessionStorage.getItem(`recipe-${id}`);
    if (raw) {
      try {
        setRecipe(JSON.parse(raw));
      } catch {
        // ignore
      }
    }
  }, [id]);

  if (!recipe) {
    return (
      <div className="container">
        <p>
          Geen recept gevonden.{" "}
          <Link to="/recepten">Terug naar generator</Link>
        </p>
      </div>
    );
  }

  const multi = recipe.supermarkets_used.length > 1;

  return (
    <div className="container recipe-detail">
      <Link to="/recepten" className="muted">← Terug naar generator</Link>

      <header className="detail-header">
        <div className="detail-image">
          <RecipeImage recipe={recipe} />
          <span className="meal-pill big">{MEAL_LABELS[recipe.meal_type] ?? recipe.meal_type}</span>
        </div>
        <div className="detail-title">
          <h1>{recipe.title}</h1>
          {recipe.description && <p className="muted">{recipe.description}</p>}
          <div className="labels detail-labels">
            <span className="label difficulty">{recipe.difficulty}</span>
            {recipe.diet_tags.map((d) => (
              <span key={d} className="label">{d}</span>
            ))}
            {recipe.health.labels.map((l) => (
              <span key={l} className={`label ${WARN_LABELS.has(l) ? "warn" : ""}`}>{l}</span>
            ))}
          </div>
          <div className="detail-meta">
            <div>⏱️ {recipe.total_time_minutes ?? "?"} min totaal ({recipe.prep_time_minutes ?? "?"} prep + {recipe.cook_time_minutes ?? "?"} koken)</div>
            <div>🍽️ {recipe.servings} porties</div>
            <div>💶 €{recipe.cost_per_serving?.toFixed(2) ?? "?"} per portie · €{recipe.total_cost?.toFixed(2) ?? "?"} totaal</div>
          </div>
        </div>
        <div className="detail-score">
          <HealthScoreBadge score={recipe.health.score} explanation={recipe.health.explanation} size={88} />
        </div>
      </header>

      <section className="card supermarket-banner">
        <h3>Boodschappen bij {recipe.supermarkets_used.length === 1 ? "" : "(meerdere)"}</h3>
        <div className="supermarket-banner-list">
          {recipe.supermarkets_used.map((s) => (
            <div key={s.slug} className="supermarket-banner-item">
              <SupermarketLogo slug={s.slug} name={s.name} size={32} />
              <span>{s.offer_count} aanbieding(en) gebruikt</span>
            </div>
          ))}
        </div>
        {multi && (
          <p className="warning">⚠️ Dit recept gebruikt aanbiedingen van meerdere supermarkten.</p>
        )}
      </section>

      {recipe.why_smart && (
        <section className="card highlight">
          <h3>💡 Waarom dit slim is met de aanbiedingen</h3>
          <p>{recipe.why_smart}</p>
        </section>
      )}

      <div className="detail-grid">
        <section className="card">
          <h2>Voedingswaarden per portie</h2>
          <ul className="nutrition-list">
            <li><span>Calorieën</span><b>{recipe.nutrition.kcal != null ? `${Math.round(recipe.nutrition.kcal)} kcal` : "?"}</b></li>
            <li><span>Eiwit</span><b>{recipe.nutrition.protein_g ?? "?"} g</b></li>
            <li><span>Koolhydraten</span><b>{recipe.nutrition.carbs_g ?? "?"} g (waarvan suiker {recipe.nutrition.sugar_g ?? "?"} g)</b></li>
            <li><span>Vet</span><b>{recipe.nutrition.fat_g ?? "?"} g (verzadigd {recipe.nutrition.saturated_fat_g ?? "?"} g)</b></li>
            <li><span>Vezels</span><b>{recipe.nutrition.fiber_g ?? "?"} g</b></li>
            <li><span>Zout</span><b>{recipe.nutrition.salt_g ?? "?"} g</b></li>
            <li className="muted"><span>Bron</span><span>{recipe.nutrition.source}</span></li>
          </ul>
        </section>

        <section className="card">
          <h2>🛒 Wat koop je in de supermarkt</h2>
          <ul className="ingredient-list">
            {recipe.shopping_items.length > 0 ? (
              recipe.shopping_items.map((s, i) => <li key={i}>{s}</li>)
            ) : (
              <li className="muted">Geen specifieke boodschappen — gebruik wat in huis is.</li>
            )}
          </ul>
        </section>

        <section className="card">
          <h2>🧂 Wat heb je waarschijnlijk al in huis</h2>
          {recipe.pantry_items.length > 0 ? (
            <ul className="ingredient-list">
              {recipe.pantry_items.map((p, i) => <li key={i}>{p}</li>)}
            </ul>
          ) : (
            <p className="muted">Geen standaardproducten nodig.</p>
          )}
          {recipe.missing_pantry_items.length > 0 && (
            <p className="warning">
              Nog te kopen: {recipe.missing_pantry_items.join(", ")}
            </p>
          )}
        </section>

        <section className="card">
          <h2>Allergenen</h2>
          {recipe.allergens.length > 0 ? (
            <div className="labels">
              {recipe.allergens.map((a) => (
                <span key={a} className="label warn">{a}</span>
              ))}
            </div>
          ) : (
            <p className="muted">Geen bekende allergenen.</p>
          )}
        </section>
      </div>

      <section className="card">
        <h2>Ingrediënten ({recipe.servings} porties)</h2>
        <ul className="ingredient-list">
          {recipe.ingredients.map((ing, i) => (
            <li key={i}>
              <span>
                <b>{ing.name}</b>
                {ing.quantity ? ` – ${ing.quantity}${ing.unit ? " " + ing.unit : ""}` : ""}
                {ing.note && <div className="muted">{ing.note}</div>}
              </span>
              <span>{ing.estimated_cost != null ? `€${ing.estimated_cost.toFixed(2)}` : ing.is_pantry ? "voorraad" : "—"}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Bereiding ({recipe.instructions.length} stappen)</h2>
        <ol className="steps">
          {recipe.instructions.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </section>

      {recipe.serving_tips.length > 0 && (
        <section className="card">
          <h2>🍴 Serveertips</h2>
          <ul className="ingredient-list">
            {recipe.serving_tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      )}

      {recipe.storage_tips.length > 0 && (
        <section className="card">
          <h2>🥡 Bewaartips</h2>
          <ul className="ingredient-list">
            {recipe.storage_tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      )}

      {recipe.variations.length > 0 && (
        <section className="card">
          <h2>🔁 Variaties</h2>
          <ul className="ingredient-list">
            {recipe.variations.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      )}
    </div>
  );
}
