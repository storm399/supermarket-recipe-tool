import { useState } from "react";
import type { Recipe } from "../types";

interface Props {
  recipe: Recipe;
  className?: string;
}

const KNOWN_KEYS = new Set([
  "default", "pasta", "salade", "curry", "zalm", "soep", "wrap", "ei",
  "ontbijt", "roerbak", "bowl", "ovenschotel", "stamppot", "smoothie",
  "gehaktballetjes", "pita",
]);

function pickImageKey(recipe: Recipe): string {
  if (recipe.image_key && KNOWN_KEYS.has(recipe.image_key)) return recipe.image_key;
  if (recipe.image_url) {
    const match = recipe.image_url.match(/\/([\w-]+)\.svg$/);
    if (match && KNOWN_KEYS.has(match[1])) return match[1];
  }
  // Fallback op basis van titel of meal_type
  const title = recipe.title.toLowerCase();
  if (title.includes("pasta") || title.includes("spaghetti")) return "pasta";
  if (title.includes("salade")) return "salade";
  if (title.includes("curry")) return "curry";
  if (title.includes("zalm") || title.includes("vis")) return "zalm";
  if (title.includes("soep")) return "soep";
  if (title.includes("wrap")) return "wrap";
  if (title.includes("omelet") || title.includes("ei") || title.includes("frittata")) return "ei";
  if (title.includes("roerbak") || title.includes("tofu")) return "roerbak";
  if (title.includes("bowl") || title.includes("falafel") || title.includes("quinoa")) return "bowl";
  if (title.includes("oven") || title.includes("schotel")) return "ovenschotel";
  if (title.includes("stamppot")) return "stamppot";
  if (title.includes("smoothie")) return "smoothie";
  if (title.includes("gehakt") || title.includes("bal")) return "gehaktballetjes";
  if (title.includes("pita")) return "pita";
  if (recipe.meal_type === "ontbijt") return "ontbijt";
  return "default";
}

export function RecipeImage({ recipe, className = "" }: Props) {
  const [errored, setErrored] = useState(false);
  const key = errored ? "default" : pickImageKey(recipe);
  return (
    <img
      src={`/recipe-images/${key}.svg`}
      alt={recipe.title}
      className={`recipe-img ${className}`}
      onError={() => setErrored(true)}
      loading="lazy"
    />
  );
}
