import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import type { Recipe } from "../types";

function scoreClass(score: number): string {
  if (score >= 75) return "high";
  if (score >= 50) return "mid";
  return "low";
}

const WARN_LABELS = new Set(["veel zout", "veel suiker"]);

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

  return (
    <div className="container">
      <Link to="/recepten" className="muted">← Terug naar receptgenerator</Link>
      <div style={{ display: "flex", alignItems: "flex-start", gap: "1rem", marginTop: "0.5rem", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 240 }}>
          <h1>{recipe.title}</h1>
          {recipe.description && <p className="muted">{recipe.description}</p>}
        </div>
        <div className={`health-score ${scoreClass(recipe.health.score)}`} style={{ width: 72, height: 72, fontSize: "1.4rem" }}>
          {recipe.health.score}
        </div>
      </div>

      <div className="labels" style={{ marginTop: "0.5rem" }}>
        {recipe.diet_tags.map((d) => (
          <span key={d} className="label">{d}</span>
        ))}
        {recipe.health.labels.map((l) => (
          <span key={l} className={`label ${WARN_LABELS.has(l) ? "warn" : ""}`}>{l}</span>
        ))}
      </div>

      <div className="card" style={{ marginTop: "1rem" }}>
        <div className="muted">{recipe.health.explanation}</div>
      </div>

      <div className="grid" style={{ gridTemplateColumns: "1fr 1fr", marginTop: "1rem", gap: "1rem" }}>
        <div className="card">
          <h2>Overzicht</h2>
          <ul className="ingredient-list">
            <li><span>Aantal porties</span><b>{recipe.servings}</b></li>
            <li><span>Bereidingstijd</span><b>{recipe.prep_time_minutes ?? "?"} min</b></li>
            <li><span>Totale kosten</span><b>{recipe.total_cost != null ? `€${recipe.total_cost.toFixed(2)}` : "-"}</b></li>
            <li><span>Kosten per portie</span><b>{recipe.cost_per_serving != null ? `€${recipe.cost_per_serving.toFixed(2)}` : "-"}</b></li>
            <li><span>Bron recept</span><b>{recipe.generated_by === "llm" ? "AI" : "Regels"}</b></li>
          </ul>
        </div>

        <div className="card">
          <h2>Voedingswaarden per portie</h2>
          <ul className="ingredient-list">
            <li><span>Calorieen</span><b>{recipe.nutrition.kcal != null ? `${Math.round(recipe.nutrition.kcal)} kcal` : "?"}</b></li>
            <li><span>Eiwit</span><b>{recipe.nutrition.protein_g ?? "?"} g</b></li>
            <li><span>Koolhydraten</span><b>{recipe.nutrition.carbs_g ?? "?"} g (waarvan suiker {recipe.nutrition.sugar_g ?? "?"} g)</b></li>
            <li><span>Vet</span><b>{recipe.nutrition.fat_g ?? "?"} g (verzadigd {recipe.nutrition.saturated_fat_g ?? "?"} g)</b></li>
            <li><span>Vezels</span><b>{recipe.nutrition.fiber_g ?? "?"} g</b></li>
            <li><span>Zout</span><b>{recipe.nutrition.salt_g ?? "?"} g</b></li>
            <li className="muted"><span>Schatting</span><span>{recipe.nutrition.source}</span></li>
          </ul>
        </div>
      </div>

      <div className="card" style={{ marginTop: "1rem" }}>
        <h2>Ingredienten</h2>
        <ul className="ingredient-list">
          {recipe.ingredients.map((ing, i) => (
            <li key={i}>
              <span>
                <b>{ing.name}</b>
                {ing.quantity ? ` – ${ing.quantity}${ing.unit ? " " + ing.unit : ""}` : ""}
                {ing.note && <div className="muted" style={{ fontSize: "0.85rem" }}>{ing.note}</div>}
              </span>
              <span>{ing.estimated_cost != null ? `€${ing.estimated_cost.toFixed(2)}` : ing.is_pantry ? "voorraad" : "-"}</span>
            </li>
          ))}
        </ul>
        {recipe.missing_pantry_items.length > 0 && (
          <p className="muted" style={{ marginTop: "0.75rem" }}>
            Nog te kopen: {recipe.missing_pantry_items.join(", ")}
          </p>
        )}
      </div>

      <div className="card" style={{ marginTop: "1rem" }}>
        <h2>Bereiding</h2>
        <ol className="steps">
          {recipe.instructions.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </div>
    </div>
  );
}
