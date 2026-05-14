import type { Supermarket } from "../types";
import { SupermarketLogo } from "./SupermarketLogo";

interface Props {
  supermarkets: Supermarket[];
  selected: string[];
  onChange: (slugs: string[]) => void;
  counts?: Record<string, number>;
}

export function SupermarketFilter({ supermarkets, selected, onChange, counts }: Props) {
  function toggle(slug: string) {
    if (selected.includes(slug)) {
      onChange(selected.filter((s) => s !== slug));
    } else {
      onChange([...selected, slug]);
    }
  }
  return (
    <div className="supermarket-filter">
      {supermarkets.map((s) => {
        const active = selected.includes(s.slug);
        return (
          <button
            type="button"
            key={s.slug}
            onClick={() => toggle(s.slug)}
            className={`supermarket-chip ${active ? "active" : ""}`}
            title={s.name}
          >
            <SupermarketLogo slug={s.slug} name={s.name} size={28} />
            {counts && (
              <span className="supermarket-chip-count">
                {counts[s.slug] ?? 0}
              </span>
            )}
          </button>
        );
      })}
      {selected.length > 0 && (
        <button type="button" className="supermarket-chip clear" onClick={() => onChange([])}>
          Wis selectie
        </button>
      )}
    </div>
  );
}
