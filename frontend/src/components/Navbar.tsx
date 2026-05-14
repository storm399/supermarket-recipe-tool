import { NavLink } from "react-router-dom";

export function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="brand">
          🥦 Supermarkt Recepten
        </NavLink>
        <nav>
          <NavLink to="/" end>
            Aanbiedingen
          </NavLink>
          <NavLink to="/recepten">Recepten</NavLink>
        </nav>
      </div>
    </header>
  );
}
