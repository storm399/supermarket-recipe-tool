import type { Recipe } from "../types";

interface Props {
  recipe: Recipe;
  onSelect?: () => void;
}

function scoreClass(score: number): string {
  if (score >= 75) return "high";
  if (score >= 50) return "mid";
  return "low";
}

const WARN_LABELS = new Set(["veel zout", "veel suiker"]);

export function RecipeCard({ recipe, onSelect }: Props) {
  return (
    <article className="card recipe-card">
      <div className="header">
        <div>
          <h3>{recipe.title}</h3>
          {recipe.description && <p className="muted">{recipe.description}</p>}
        </div>
        <div className={`health-score ${scoreClass(recipe.health.score)}`} title={recipe.health.explanation}>
          {recipe.health.score}
        </div>
      </div>
      <div className="stats">
        <div>
          <b>{recipe.nutrition.kcal != null ? Math.round(recipe.nutrition.kcal) : "?"}</b>
          kcal / portie
        </div>
        <div>
          <b>{recipe.nutrition.protein_g != null ? Math.round(recipe.nutrition.protein_g) : "?"} g</b>
          eiwit
        </div>
        <div>
          <b>{recipe.cost_per_serving != null ? `€${recipe.cost_per_serving.toFixed(2)}` : "?"}</b>
          per portie
        </div>
      </div>
      {recipe.health.labels.length > 0 && (
        <div className="labels">
          {recipe.health.labels.map((l) => (
            <span key={l} className={`label ${WARN_LABELS.has(l) ? "warn" : ""}`}>{l}</span>
          ))}
        </div>
      )}
      <div className="muted" style={{ fontSize: "0.85rem" }}>{recipe.health.explanation}</div>
      {onSelect && (
        <button className="primary" onClick={onSelect}>
          Bekijk recept
        </button>
      )}
    </article>
  );
}
