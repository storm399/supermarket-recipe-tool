interface Props {
  score: number;
  explanation?: string;
  size?: number;
}

export function HealthScoreBadge({ score, explanation, size = 56 }: Props) {
  const cls = score >= 75 ? "high" : score >= 50 ? "mid" : "low";
  return (
    <div
      className={`health-badge ${cls}`}
      style={{ width: size, height: size, fontSize: size * 0.32 }}
      title={explanation}
      aria-label={`Gezondheidsscore ${score} van 100`}
    >
      <span>{score}</span>
      <small>/100</small>
    </div>
  );
}
