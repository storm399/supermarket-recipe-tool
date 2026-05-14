export interface Supermarket {
  id: number;
  slug: string;
  name: string;
  logo_url: string | null;
  active: boolean;
}

export interface Offer {
  id: number;
  product_name: string;
  category: string | null;
  unit: string | null;
  amount: number | null;
  original_price: number | null;
  sale_price: number;
  discount_percent: number | null;
  discount_text: string | null;
  valid_from: string | null;
  valid_until: string | null;
  image_url: string | null;
  source_url: string | null;
  source: string;
  fetched_at: string;
  supermarket: Supermarket;
}

export interface ScrapeResult {
  supermarket: string;
  source: string;
  fetched: number;
  saved: number;
  duplicates_skipped: number;
  ok: boolean;
  error: string | null;
  duration_ms: number;
}

export interface RefreshResponse {
  ok: boolean;
  total: number;
  results: ScrapeResult[];
}

export interface OfferList {
  total: number;
  offers: Offer[];
}

export interface OfferStats {
  total: number;
  by_supermarket: Record<string, number>;
  by_category: Record<string, number>;
  average_discount_percent: number | null;
  source: string;
}

export interface RecipeIngredient {
  name: string;
  quantity: number | null;
  unit: string | null;
  is_pantry: boolean;
  estimated_cost: number | null;
  offer_id: number | null;
  note: string | null;
  supermarket_slug: string | null;
  supermarket_name: string | null;
  offer_product_name: string | null;
}

export interface Nutrition {
  kcal: number | null;
  protein_g: number | null;
  carbs_g: number | null;
  sugar_g: number | null;
  fat_g: number | null;
  saturated_fat_g: number | null;
  fiber_g: number | null;
  salt_g: number | null;
  source: string;
}

export interface Health {
  score: number;
  explanation: string;
  labels: string[];
}

export interface RecipeSupermarketUse {
  slug: string;
  name: string;
  offer_count: number;
}

export type MealType = "ontbijt" | "lunch" | "diner" | "snack" | "meal-prep";
export type Difficulty = "makkelijk" | "gemiddeld" | "uitdagend";

export interface Recipe {
  id: number | null;
  title: string;
  description: string | null;
  meal_type: MealType;
  difficulty: Difficulty;
  instructions: string[];
  servings: number;
  prep_time_minutes: number | null;
  cook_time_minutes: number | null;
  total_time_minutes: number | null;
  total_cost: number | null;
  cost_per_serving: number | null;
  diet_tags: string[];
  missing_pantry_items: string[];
  allergens: string[];
  serving_tips: string[];
  storage_tips: string[];
  variations: string[];
  ingredients: RecipeIngredient[];
  supermarkets_used: RecipeSupermarketUse[];
  why_smart: string | null;
  shopping_items: string[];
  pantry_items: string[];
  image_url: string | null;
  image_key: string | null;
  nutrition: Nutrition;
  health: Health;
  generated_by: string;
  generated_at: string | null;
}

export type DietTag =
  | "vegetarisch"
  | "vegan"
  | "halal"
  | "lactosevrij"
  | "glutenvrij";

export interface RecipeRequest {
  servings: number;
  diets: DietTag[];
  meal_types: MealType[];
  max_prep_minutes: number | null;
  min_protein_g: number | null;
  max_kcal_per_serving: number | null;
  max_budget_per_serving: number | null;
  min_health_score: number | null;
  selected_supermarkets: string[];
  allow_multi_supermarket: boolean;
  exclude_ingredients: string[];
  count: number;
  sort: "smart" | "health-desc" | "price-asc" | "time-asc";
  use_llm: boolean;
}

export type OfferSort = "price-asc" | "price-desc" | "discount-desc" | "name-asc";
