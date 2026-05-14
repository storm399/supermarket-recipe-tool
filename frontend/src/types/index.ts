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
  fetched_at: string;
  supermarket: Supermarket;
}

export interface OfferList {
  total: number;
  offers: Offer[];
}

export interface RecipeIngredient {
  name: string;
  quantity: number | null;
  unit: string | null;
  is_pantry: boolean;
  estimated_cost: number | null;
  offer_id: number | null;
  note: string | null;
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

export interface Recipe {
  id: number | null;
  title: string;
  description: string | null;
  instructions: string[];
  servings: number;
  prep_time_minutes: number | null;
  total_cost: number | null;
  cost_per_serving: number | null;
  diet_tags: string[];
  missing_pantry_items: string[];
  ingredients: RecipeIngredient[];
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
  max_prep_minutes: number | null;
  min_protein_g: number | null;
  max_kcal_per_serving: number | null;
  max_budget_per_serving: number | null;
  favorite_supermarkets: string[];
  exclude_ingredients: string[];
  count: number;
  use_llm: boolean;
}
