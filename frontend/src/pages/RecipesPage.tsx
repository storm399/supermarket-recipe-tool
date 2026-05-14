import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../api/client";
import { RecipeCard } from "../components/RecipeCard";
import type { DietTag, Recipe, Supermarket } from "../types";

const DIET_OPTIONS: DietTag[] = [
  "vegetarisch",
  "vegan",
  "halal",
  "lactosevrij",
  "glutenvrij",
];

export default function RecipesPage() {
  const [supermarkets, setSupermarkets] = useState<Supermarket[]>([]);
  const [servings, setServings] = useState(2);
  const [diets, setDiets] = useState<DietTag[]>([]);
  const [maxPrep, setMaxPrep] = useState<string>("");
  const [minProtein, setMinProtein] = useState<string>("");
  const [maxKcal, setMaxKcal] = useState<string>("");
  const [maxBudget, setMaxBudget] = useState<string>("");
  const [favSm, setFavSm] = useState<string[]>([]);
  const [exclude, setExclude] = useState<string>("");
  const [count, setCount] = useState(3);
  const [useLlm, setUseLlm] = useState(false);
  const [llmAvailable, setLlmAvailable] = useState(false);

  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.supermarkets().then(setSupermarkets).catch(() => {});
    api.recipesHealth().then((h) => setLlmAvailable(h.llm_available)).catch(() => {});
  }, []);

  function toggle<T>(value: T, list: T[], set: (l: T[]) => void) {
    set(list.includes(value) ? list.filter((v) => v !== value) : [...list, value]);
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await api.generateRecipes({
        servings,
        count,
        diets,
        max_prep_minutes: maxPrep ? Number(maxPrep) : null,
        min_protein_g: minProtein ? Number(minProtein) : null,
        max_kcal_per_serving: maxKcal ? Number(maxKcal) : null,
        max_budget_per_serving: maxBudget ? Number(maxBudget) : null,
        favorite_supermarkets: favSm,
        exclude_ingredients: exclude
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        use_llm: useLlm && llmAvailable,
      });
      setRecipes(result);
      if (result.length === 0) {
        setError("Geen recepten gevonden met deze filters. Probeer minder strenge filters.");
      }
    } catch (e: any) {
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  function openDetail(r: Recipe, idx: number) {
    sessionStorage.setItem(`recipe-${idx}`, JSON.stringify(r));
    navigate(`/recepten/${idx}`);
  }

  return (
    <div className="container">
      <h1>Receptgenerator</h1>
      <p className="muted">
        Combineer actuele aanbiedingen tot voedzame recepten met gezondheidsscore.
      </p>

      <form className="card" onSubmit={onSubmit}>
        <div className="filters">
          <label>
            Aantal personen
            <input type="number" min={1} max={12} value={servings} onChange={(e) => setServings(Number(e.target.value))} />
          </label>
          <label>
            Aantal recepten
            <input type="number" min={1} max={10} value={count} onChange={(e) => setCount(Number(e.target.value))} />
          </label>
          <label>
            Max bereiding (min)
            <input type="number" min={5} max={240} value={maxPrep} onChange={(e) => setMaxPrep(e.target.value)} placeholder="bv 30" />
          </label>
          <label>
            Min eiwit per portie (g)
            <input type="number" min={0} value={minProtein} onChange={(e) => setMinProtein(e.target.value)} placeholder="bv 20" />
          </label>
          <label>
            Max kcal per portie
            <input type="number" min={0} value={maxKcal} onChange={(e) => setMaxKcal(e.target.value)} placeholder="bv 700" />
          </label>
          <label>
            Max budget per portie (€)
            <input type="number" min={0} step="0.1" value={maxBudget} onChange={(e) => setMaxBudget(e.target.value)} placeholder="bv 3.50" />
          </label>
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <strong>Dieetwensen</strong>
          <div className="checkboxes">
            {DIET_OPTIONS.map((d) => (
              <label key={d}>
                <input type="checkbox" checked={diets.includes(d)} onChange={() => toggle(d, diets, setDiets)} />
                {d}
              </label>
            ))}
          </div>
        </div>

        <div style={{ marginTop: "0.75rem" }}>
          <strong>Favoriete supermarkten</strong>
          <div className="checkboxes">
            {supermarkets.map((s) => (
              <label key={s.slug}>
                <input type="checkbox" checked={favSm.includes(s.slug)} onChange={() => toggle(s.slug, favSm, setFavSm)} />
                {s.name}
              </label>
            ))}
          </div>
        </div>

        <div style={{ marginTop: "0.75rem" }}>
          <label>
            Ingredienten uitsluiten (komma-gescheiden)
            <input type="text" value={exclude} onChange={(e) => setExclude(e.target.value)} placeholder="bv. zalm, kaas" />
          </label>
        </div>

        {llmAvailable && (
          <div style={{ marginTop: "0.75rem" }}>
            <label className="checkboxes" style={{ display: "inline-flex" }}>
              <input type="checkbox" checked={useLlm} onChange={(e) => setUseLlm(e.target.checked)} />
              Gebruik AI-receptgenerator
            </label>
          </div>
        )}

        <div className="spacer" />
        <button className="primary" type="submit" disabled={loading}>
          {loading ? "Recepten genereren…" : "Genereer recepten"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {recipes.length > 0 && (
        <>
          <h2 style={{ marginTop: "1.5rem" }}>Voorgestelde recepten</h2>
          <div className="grid recipes">
            {recipes.map((r, i) => (
              <RecipeCard key={i} recipe={r} onSelect={() => openDetail(r, i)} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
