interface QuickFilter<T> {
  key: string;
  label: string;
  icon?: string;
  apply: (value: T) => Partial<T>;
}

interface Props<T> {
  filters: QuickFilter<T>[];
  state: T;
  onApply: (patch: Partial<T>) => void;
}

export function QuickFilters<T>({ filters, state, onApply }: Props<T>) {
  return (
    <div className="quick-filters" role="group" aria-label="Snelle filters">
      {filters.map((f) => (
        <button
          type="button"
          key={f.key}
          className="quick-filter"
          onClick={() => onApply(f.apply(state))}
        >
          {f.icon && <span aria-hidden>{f.icon}</span>}
          {f.label}
        </button>
      ))}
    </div>
  );
}
