interface Props {
  source: string;
  size?: "small" | "normal";
}

const LABELS: Record<string, { label: string; cls: string; icon: string }> = {
  live_scraper: { label: "Live", cls: "source-live", icon: "🟢" },
  public_api: { label: "API", cls: "source-live", icon: "🟢" },
  manual_seed: { label: "Seed", cls: "source-seed", icon: "🌱" },
  fallback_mock: { label: "Mock", cls: "source-mock", icon: "🧪" },
  live: { label: "Live", cls: "source-live", icon: "🟢" },
  mock: { label: "Mockdata", cls: "source-mock", icon: "🧪" },
};

export function SourceBadge({ source, size = "normal" }: Props) {
  const def = LABELS[source] ?? LABELS.fallback_mock;
  return (
    <span className={`source-badge ${def.cls} ${size === "small" ? "small" : ""}`} title={`Bron: ${source}`}>
      <span aria-hidden>{def.icon}</span>
      {def.label}
    </span>
  );
}
