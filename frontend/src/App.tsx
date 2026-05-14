import { Route, Routes } from "react-router-dom";

import { Navbar } from "./components/Navbar";
import OffersPage from "./pages/OffersPage";
import RecipeDetailPage from "./pages/RecipeDetailPage";
import RecipesPage from "./pages/RecipesPage";

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<OffersPage />} />
          <Route path="/recepten" element={<RecipesPage />} />
          <Route path="/recepten/:id" element={<RecipeDetailPage />} />
          <Route path="*" element={<OffersPage />} />
        </Routes>
      </main>
    </>
  );
}
