import { Route, Routes } from "react-router-dom";

import { Navbar } from "./components/Navbar";
import FavoritesPage from "./pages/FavoritesPage";
import HomePage from "./pages/HomePage";
import OffersPage from "./pages/OffersPage";
import RecipeDetailPage from "./pages/RecipeDetailPage";
import RecipesPage from "./pages/RecipesPage";

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/aanbiedingen" element={<OffersPage />} />
          <Route path="/recepten" element={<RecipesPage />} />
          <Route path="/recepten/:id" element={<RecipeDetailPage />} />
          <Route path="/favorieten" element={<FavoritesPage />} />
          <Route path="*" element={<HomePage />} />
        </Routes>
      </main>
      <footer className="site-footer">
        <p>
          Supermarkt Recepten Tool · Slim koken met aanbiedingen ·{" "}
          <a href="https://github.com/storm399/supermarket-recipe-tool" target="_blank" rel="noreferrer">GitHub</a>
        </p>
      </footer>
    </>
  );
}
