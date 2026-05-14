import { useState } from "react";
import type { Recipe } from "../types";

interface Props {
  recipe: Recipe;
  className?: string;
}

const KNOWN_SVG_KEYS = new Set([
  "default", "pasta", "salade", "curry", "zalm", "soep", "wrap", "ei",
  "ontbijt", "roerbak", "bowl", "ovenschotel", "stamppot", "smoothie",
  "gehaktballetjes", "pita",
]);

function pickFallbackKey(recipe: Recipe): string {
  if (recipe.image_key && KNOWN_SVG_KEYS.has(recipe.image_key)) return recipe.image_key;
  const title = recipe.title.toLowerCase();
  if (title.includes("pasta") || title.includes("spaghetti") || title.includes("lasagne") || title.includes("macaroni")) return "pasta";
  if (title.includes("salade") || title.includes("bulgur")) return "salade";
  if (title.includes("curry")) return "curry";
  if (title.includes("zalm") || title.includes("kabeljauw") || title.includes("vis")) return "zalm";
  if (title.includes("soep") || title.includes("erwten")) return "soep";
  if (title.includes("wrap") || title.includes("taco")) return "wrap";
  if (title.includes("omelet") || title.includes("ei") || title.includes("frittata") || title.includes("pannenkoek")) return "ei";
  if (title.includes("roerbak") || title.includes("tofu") || title.includes("ramen")) return "roerbak";
  if (title.includes("bowl") || title.includes("falafel") || title.includes("quinoa")) return "bowl";
  if (title.includes("oven") || title.includes("schotel") || title.includes("gevulde paprika") || title.includes("frietjes") || title.includes("risotto") || title.includes("pesto-aardap")) return "ovenschotel";
  if (title.includes("stamppot") || title.includes("stoofvlees")) return "stamppot";
  if (title.includes("smoothie") || title.includes("yoghurt")) return "smoothie";
  if (title.includes("gehakt") || title.includes("bal")) return "gehaktballetjes";
  if (title.includes("pita") || title.includes("pizza")) return "pita";
  if (recipe.meal_type === "ontbijt") return "ontbijt";
  return "default";
}

/**
 * Toont eerst een externe foto (image_url, vaak Unsplash). Bij fout
 * (offline, blokkering, 404) valt het automatisch terug op de lokale
 * SVG-illustratie via een heuristiek op titel/meal_type.
 */
export function RecipeImage({ recipe, className = "" }: Props) {
  const [stage, setStage] = useState<"remote" | "fallback">("remote");

  const remoteSrc = recipe.image_url || "";
  const isRemote = remoteSrc.startsWith("http");
  const fallbackSrc = `/recipe-images/${pickFallbackKey(recipe)}.svg`;
  const src = stage === "remote" && isRemote ? remoteSrc : fallbackSrc;

  return (
    <img
      src={src}
      alt={recipe.title}
      className={`recipe-img ${className}`}
      onError={() => setStage("fallback")}
      loading="lazy"
    />
  );
}
