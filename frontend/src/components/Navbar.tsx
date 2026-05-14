import { NavLink } from "react-router-dom";

export function Navbar() {
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
        </nav>
      </div>
    </header>
  );
}
