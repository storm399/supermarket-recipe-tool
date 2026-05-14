interface Props {
  count?: number;
  variant?: "offer" | "recipe";
}

export function LoadingSkeleton({ count = 6, variant = "offer" }: Props) {
  return (
    <div className={variant === "recipe" ? "grid recipes" : "grid offers"}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className={`skeleton skeleton-${variant}`}>
          <div className="skeleton-img" />
          <div className="skeleton-line w70" />
          <div className="skeleton-line w50" />
          <div className="skeleton-line w90" />
        </div>
      ))}
    </div>
  );
}
