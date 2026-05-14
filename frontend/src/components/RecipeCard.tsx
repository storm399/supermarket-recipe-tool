import type { Recipe } from "../types";
import { HealthScoreBadge } from "./HealthScoreBadge";
import { RecipeImage } from "./RecipeImage";
import { SupermarketLogo } from "./SupermarketLogo";

interface Props {
  recipe: Recipe;
  onSelect?: () => void;
}

const WARN_LABELS = new Set(["veel zout", "veel suiker"]);
const MEAL_LABELS: Record<string, string> = {
  ontbijt: "Ontbijt",
  lunch: "Lunch",
  diner: "Diner",
  snack: "Snack",
  "meal-prep": "Meal prep",
};

export function RecipeCard({ recipe, onSelect }: Props) {
  const multiSuper = recipe.supermarkets_used.length > 1;
  return (
    <article className="recipe-card" onClick={onSelect} role={onSelect ? "button" : undefined}>
      <div className="recipe-card-img">
        <RecipeImage recipe={recipe} />
        <span className="meal-pill">{MEAL_LABELS[recipe.meal_type] ?? recipe.meal_type}</span>
        <div className="recipe-card-score">
          <HealthScoreBadge score={recipe.health.score} explanation={recipe.health.explanation} size={52} />
        </div>
      </div>
      <div className="recipe-card-body">
        <h3 className="recipe-title">{recipe.title}</h3>
        {recipe.description && <p className="recipe-desc">{recipe.description}</p>}
        <div className="recipe-stats">
          <div>
            <b>{recipe.total_time_minutes ?? "?"} min</b>
            <small>totale tijd</small>
          </div>
          <div>
            <b>{recipe.nutrition.kcal != null ? Math.round(recipe.nutrition.kcal) : "?"}</b>
            <small>kcal/portie</small>
          </div>
          <div>
            <b>{recipe.nutrition.protein_g != null ? Math.round(recipe.nutrition.protein_g) : "?"} g</b>
            <small>eiwit</small>
          </div>
          <div>
            <b>{recipe.cost_per_serving != null ? `€${recipe.cost_per_serving.toFixed(2)}` : "?"}</b>
            <small>per portie</small>
          </div>
        </div>
        <div className="recipe-card-supermarkets">
          {recipe.supermarkets_used.map((s) => (
            <span key={s.slug} className="supermarket-tag-row" title={`${s.offer_count} aanbieding(en)`}>
              <SupermarketLogo slug={s.slug} name={s.name} size={20} />
              <small>{s.offer_count}×</small>
            </span>
          ))}
          {multiSuper && (
            <span className="multi-warning" title="Recept gebruikt meerdere supermarkten">⚠️ meerdere winkels</span>
          )}
        </div>
        {recipe.health.labels.length > 0 && (
          <div className="recipe-labels">
            {recipe.health.labels.slice(0, 4).map((l) => (
              <span key={l} className={`label ${WARN_LABELS.has(l) ? "warn" : ""}`}>{l}</span>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}
