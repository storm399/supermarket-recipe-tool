import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../api/client";
import { EmptyState } from "../components/EmptyState";
import { LoadingSkeleton } from "../components/LoadingSkeleton";
import { RecipeCard } from "../components/RecipeCard";
import { SupermarketFilter } from "../components/SupermarketFilter";
import type { DietTag, MealType, Recipe, Supermarket } from "../types";

const DIET_OPTIONS: DietTag[] = ["vegetarisch", "vegan", "halal", "lactosevrij", "glutenvrij"];
const MEAL_OPTIONS: { value: MealType; label: string }[] = [
  { value: "ontbijt", label: "Ontbijt" },
  { value: "lunch", label: "Lunch" },
  { value: "diner", label: "Diner" },
  { value: "snack", label: "Snack" },
  { value: "meal-prep", label: "Meal prep" },
];
const COUNT_OPTIONS = [6, 12, 24];

export default function RecipesPage() {
  const [supermarkets, setSupermarkets] = useState<Supermarket[]>([]);
  const [servings, setServings] = useState(2);
  const [diets, setDiets] = useState<DietTag[]>([]);
  const [mealTypes, setMealTypes] = useState<MealType[]>([]);
  const [maxPrep, setMaxPrep] = useState<string>("");
  const [minProtein, setMinProtein] = useState<string>("");
  const [maxKcal, setMaxKcal] = useState<string>("");
  const [maxBudget, setMaxBudget] = useState<string>("");
  const [minHealth, setMinHealth] = useState<string>("");
  const [selectedSm, setSelectedSm] = useState<string[]>([]);
  const [allowMulti, setAllowMulti] = useState(false);
  const [exclude, setExclude] = useState<string>("");
  const [count, setCount] = useState(12);
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
    setRecipes([]);
    try {
      const result = await api.generateRecipes({
        servings,
        count,
        diets,
        meal_types: mealTypes,
        max_prep_minutes: maxPrep ? Number(maxPrep) : null,
        min_protein_g: minProtein ? Number(minProtein) : null,
        max_kcal_per_serving: maxKcal ? Number(maxKcal) : null,
        max_budget_per_serving: maxBudget ? Number(maxBudget) : null,
        min_health_score: minHealth ? Number(minHealth) : null,
        selected_supermarkets: selectedSm,
        allow_multi_supermarket: allowMulti,
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
      <header className="page-head">
        <div>
          <h1>Recepten genereren</h1>
          <p className="muted">Combineer aanbiedingen tot 12+ recepten met voedingsinfo en gezondheidsscore.</p>
        </div>
      </header>

      <form className="card filter-card" onSubmit={onSubmit}>
        <h2>1. Kies je supermarkt(en)</h2>
        <p className="muted">
          Eén supermarkt selecteren? Dan krijg je alleen recepten met aanbiedingen
          uit die winkel — niet langs vijf winkels rennen.
        </p>
        <SupermarketFilter
          supermarkets={supermarkets}
          selected={selectedSm}
          onChange={setSelectedSm}
        />
        <label className="checkbox-label toggle">
          <input type="checkbox" checked={allowMulti} onChange={(e) => setAllowMulti(e.target.checked)} />
          Combineren over meerdere supermarkten toestaan
        </label>

        <h2 style={{ marginTop: "1.5rem" }}>2. Wat voor recepten?</h2>
        <div className="filters">
          <label>
            Aantal recepten
            <select value={count} onChange={(e) => setCount(Number(e.target.value))}>
              {COUNT_OPTIONS.map((n) => (
                <option key={n} value={n}>{n} recepten</option>
              ))}
            </select>
          </label>
          <label>
            Aantal personen
            <input type="number" min={1} max={12} value={servings} onChange={(e) => setServings(Number(e.target.value))} />
          </label>
          <label>
            Max bereidingstijd (min)
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
          <label>
            Min gezondheidsscore
            <input type="number" min={0} max={100} value={minHealth} onChange={(e) => setMinHealth(e.target.value)} placeholder="bv 70" />
          </label>
        </div>

        <div className="filter-group">
          <strong>Maaltijdtypes</strong>
          <div className="checkboxes">
            {MEAL_OPTIONS.map((m) => (
              <label key={m.value}>
                <input type="checkbox" checked={mealTypes.includes(m.value)} onChange={() => toggle(m.value, mealTypes, setMealTypes)} />
                {m.label}
              </label>
            ))}
          </div>
        </div>

        <div className="filter-group">
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

        <div className="filter-group">
          <label>
            Ingrediënten uitsluiten (komma-gescheiden)
            <input type="text" value={exclude} onChange={(e) => setExclude(e.target.value)} placeholder="bv. zalm, kaas" />
          </label>
        </div>

        {llmAvailable && (
          <label className="checkbox-label toggle">
            <input type="checkbox" checked={useLlm} onChange={(e) => setUseLlm(e.target.checked)} />
            Gebruik AI-receptgenerator (experimenteel)
          </label>
        )}

        <button className="primary btn-large" type="submit" disabled={loading}>
          {loading ? "Bezig met genereren…" : `Genereer ${count} recepten`}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {loading && <LoadingSkeleton count={count} variant="recipe" />}

      {!loading && recipes.length === 0 && !error && (
        <EmptyState
          icon="👨‍🍳"
          title="Klaar om te koken?"
          message="Vul je voorkeuren in en klik op 'Genereer recepten' om aan de slag te gaan."
        />
      )}

      {recipes.length > 0 && (
        <>
          <h2 style={{ marginTop: "1.5rem" }}>{recipes.length} voorgestelde recepten</h2>
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
