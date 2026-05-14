import { useState } from "react";

interface Props {
  slug: string;
  name: string;
  size?: number;
  className?: string;
}

export function SupermarketLogo({ slug, name, size = 36, className = "" }: Props) {
  const [errored, setErrored] = useState(false);
  const src = `/logos/${slug}.svg`;

  if (errored) {
    return (
      <div
        className={`logo-fallback ${className}`}
        style={{ width: size * 2, height: size, lineHeight: `${size}px` }}
        aria-label={name}
        title={name}
      >
        {name}
      </div>
    );
  }

  return (
    <img
      src={src}
      alt={name}
      title={name}
      className={`logo ${className}`}
      onError={() => setErrored(true)}
      style={{ height: size, width: "auto" }}
    />
  );
}
