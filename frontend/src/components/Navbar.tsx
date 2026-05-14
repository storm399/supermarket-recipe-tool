import { NavLink } from "react-router-dom";
import { useFavorites } from "../hooks/useFavorites";

export function Navbar() {
  const { list } = useFavorites();
  const favCount = list().length;
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="brand">
          <span className="brand-emoji" aria-hidden>🥦</span>
          <span>Supermarkt<strong>Recepten</strong></span>
        </NavLink>
        <nav>
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/aanbiedingen">Aanbiedingen</NavLink>
          <NavLink to="/recepten">Recepten</NavLink>
          <NavLink to="/favorieten">
            Favorieten {favCount > 0 && <span className="nav-badge">{favCount}</span>}
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
