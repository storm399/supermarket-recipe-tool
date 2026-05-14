import { useNavigate } from "react-router-dom";
import { EmptyState } from "../components/EmptyState";
import { RecipeCard } from "../components/RecipeCard";
import { useFavorites } from "../hooks/useFavorites";
import type { Recipe } from "../types";

export default function FavoritesPage() {
  const { list, clear } = useFavorites();
  const favorites = list();
  const navigate = useNavigate();

  function openDetail(r: Recipe, idx: number) {
    sessionStorage.setItem(`recipe-${idx}`, JSON.stringify(r));
    navigate(`/recepten/${idx}`);
  }

  return (
    <div className="container">
      <header className="page-head">
        <div>
          <h1>Mijn favorieten</h1>
          <p className="muted">
            {favorites.length === 0
              ? "Nog geen recepten bewaard."
              : `${favorites.length} bewaarde ${favorites.length === 1 ? "recept" : "recepten"}.`}
          </p>
        </div>
        {favorites.length > 0 && (
          <button onClick={() => {
            if (window.confirm("Alle favorieten verwijderen?")) clear();
          }}>
            Wis alles
          </button>
        )}
      </header>

      {favorites.length === 0 ? (
        <EmptyState
          icon="♥"
          title="Bewaar je favoriete recepten"
          message="Klik op het hartje bij een recept om het hier te bewaren. Zo heb je je vaste lijst altijd binnen handbereik."
          actionLabel="Naar receptgenerator"
          onAction={() => navigate("/recepten")}
        />
      ) : (
        <div className="grid recipes">
          {favorites.map((r, i) => (
            <RecipeCard key={r.title} recipe={r} onSelect={() => openDetail(r, i)} />
          ))}
        </div>
      )}
    </div>
  );
}
