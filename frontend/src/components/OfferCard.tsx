import type { Offer } from "../types";
import { SupermarketLogo } from "./SupermarketLogo";

interface Props {
  offer: Offer;
}

function formatAmount(o: Offer): string {
  if (!o.amount || !o.unit) return "";
  return `${o.amount} ${o.unit}`;
}

export function OfferCard({ offer }: Props) {
  return (
    <article className="offer-card">
      <header className="offer-card-head">
        <SupermarketLogo slug={offer.supermarket.slug} name={offer.supermarket.name} size={26} />
        {offer.discount_percent && offer.discount_percent > 0 && (
          <span className="offer-badge">-{Math.round(offer.discount_percent)}%</span>
        )}
      </header>
      <h3 className="offer-name">{offer.product_name}</h3>
      <div className="offer-amount">{formatAmount(offer) || (offer.category ?? "")}</div>
      <div className="offer-price-row">
        <span className="offer-price">€{offer.sale_price.toFixed(2)}</span>
        {offer.original_price && offer.original_price > offer.sale_price && (
          <span className="offer-original">€{offer.original_price.toFixed(2)}</span>
        )}
      </div>
      {offer.discount_text && <div className="offer-discount-text">{offer.discount_text}</div>}
    </article>
  );
}
