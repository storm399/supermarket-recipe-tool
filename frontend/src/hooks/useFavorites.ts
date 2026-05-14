import { useCallback, useEffect, useState } from "react";
import type { Recipe } from "../types";

const KEY = "favorite-recipes-v1";

function recipeId(r: Recipe): string {
  return `${r.title}::${r.servings}`;
}

function load(): Record<string, Recipe> {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return {};
    return JSON.parse(raw) as Record<string, Recipe>;
  } catch {
    return {};
  }
}

function save(map: Record<string, Recipe>): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(map));
  } catch {
    // quota? ignore
  }
}

export function useFavorites() {
  const [favorites, setFavorites] = useState<Record<string, Recipe>>({});

  useEffect(() => {
    setFavorites(load());
  }, []);

  const isFavorite = useCallback(
    (recipe: Recipe) => recipeId(recipe) in favorites,
    [favorites]
  );

  const toggle = useCallback((recipe: Recipe) => {
    setFavorites((prev) => {
      const id = recipeId(recipe);
      const next = { ...prev };
      if (id in next) delete next[id];
      else next[id] = recipe;
      save(next);
      return next;
    });
  }, []);

  const list = useCallback(() => Object.values(favorites), [favorites]);
  const clear = useCallback(() => {
    setFavorites({});
    save({});
  }, []);

  return { favorites, list, isFavorite, toggle, clear };
}

export { recipeId };
