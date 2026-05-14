interface Chip {
  key: string;
  label: string;
  onRemove: () => void;
}

interface Props {
  chips: Chip[];
  onClearAll?: () => void;
}

export function FilterChips({ chips, onClearAll }: Props) {
  if (chips.length === 0) return null;
  return (
    <div className="filter-chips">
      <span className="filter-chips-label">Filters:</span>
      {chips.map((c) => (
        <button key={c.key} className="filter-chip" onClick={c.onRemove} type="button">
          {c.label} <span aria-hidden>✕</span>
        </button>
      ))}
      {onClearAll && (
        <button className="filter-chip clear" onClick={onClearAll} type="button">
          Alles wissen
        </button>
      )}
    </div>
  );
}
