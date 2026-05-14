import type { Offer } from "../types";

interface Props {
  offer: Offer;
}

function formatAmount(o: Offer): string {
  if (!o.amount || !o.unit) return "";
  return `${o.amount} ${o.unit}`;
}

export function OfferCard({ offer }: Props) {
  return (
    <div className="offer">
      <p className="name">{offer.product_name}</p>
      {formatAmount(offer) && <div className="muted">{formatAmount(offer)}</div>}
      <div className="price-row">
        <span className="price">€{offer.sale_price.toFixed(2)}</span>
        {offer.original_price && offer.original_price > offer.sale_price && (
          <span className="original">€{offer.original_price.toFixed(2)}</span>
        )}
        {offer.discount_percent && (
          <span className="badge">-{Math.round(offer.discount_percent)}%</span>
        )}
      </div>
      <div className="supermarket-tag">{offer.supermarket.name}</div>
      {offer.discount_text && <div className="muted">{offer.discount_text}</div>}
    </div>
  );
}
