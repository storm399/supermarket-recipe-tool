"""Transparante gezondheidsscore voor recepten.

Score 0-100. Hogere score = gezonder.
Gebaseerd op richtlijnen rond:
  - kcal per portie (te hoog = strafpunten)
  - eiwitgehalte (meer is beter, tot een plafond)
  - vezels (meer is beter)
  - aandeel groente/fruit
  - verzadigd vet (te veel = strafpunten)
  - zout (te veel = strafpunten)
  - suiker (te veel = strafpunten)
  - mate van ultrabewerking (heuristisch op categorie)

De berekening staat bewust uitgeschreven en is volledig testbaar.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HealthScoreInput:
    kcal_per_serving: float
    protein_g: float
    fiber_g: float
    saturated_fat_g: float
    salt_g: float
    sugar_g: float
    veg_fruit_grams_per_serving: float = 0.0
    ultra_processed_ratio: float = 0.0  # 0..1, fractie ultrabewerkte ingredienten op totaal gewicht


@dataclass
class HealthScoreResult:
    score: int
    explanation: str
    labels: list[str]


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def compute_health_score(data: HealthScoreInput) -> HealthScoreResult:
    score = 50.0
    reasons: list[str] = []
    labels: list[str] = []

    # kcal per portie
    if data.kcal_per_serving <= 0:
        pass
    elif data.kcal_per_serving < 350:
        score += 10
        labels.append("caloriearm")
        reasons.append("relatief weinig calorieen per portie")
    elif data.kcal_per_serving < 600:
        score += 5
    elif data.kcal_per_serving < 800:
        score -= 5
        reasons.append("redelijk calorierijk")
    else:
        score -= 15
        reasons.append("zeer calorierijk")

    # eiwit
    if data.protein_g >= 25:
        score += 12
        labels.append("eiwitrijk")
        reasons.append("hoog eiwitgehalte")
    elif data.protein_g >= 15:
        score += 7
        labels.append("eiwitrijk")
    elif data.protein_g < 8:
        score -= 5
        reasons.append("weinig eiwit")

    # vezels
    if data.fiber_g >= 8:
        score += 10
        labels.append("vezelrijk")
        reasons.append("veel vezels")
    elif data.fiber_g >= 5:
        score += 5
    elif data.fiber_g < 2:
        score -= 5
        reasons.append("weinig vezels")

    # groente / fruit
    if data.veg_fruit_grams_per_serving >= 250:
        score += 8
        reasons.append("ruime portie groente/fruit")
    elif data.veg_fruit_grams_per_serving >= 150:
        score += 4
    elif data.veg_fruit_grams_per_serving < 50:
        score -= 4
        reasons.append("weinig groente/fruit")

    # verzadigd vet
    if data.saturated_fat_g >= 10:
        score -= 12
        reasons.append("veel verzadigd vet")
    elif data.saturated_fat_g >= 6:
        score -= 6
    elif data.saturated_fat_g < 3:
        score += 4

    # zout
    if data.salt_g >= 3:
        score -= 12
        labels.append("veel zout")
        reasons.append("hoog zoutgehalte")
    elif data.salt_g >= 2:
        score -= 6
        labels.append("veel zout")
    elif data.salt_g < 1:
        score += 4

    # suiker
    if data.sugar_g >= 25:
        score -= 10
        labels.append("veel suiker")
        reasons.append("hoog suikergehalte")
    elif data.sugar_g >= 15:
        score -= 5
        labels.append("veel suiker")
    elif data.sugar_g < 6:
        score += 3

    # ultrabewerking
    if data.ultra_processed_ratio >= 0.5:
        score -= 10
        reasons.append("veel ultrabewerkte ingredienten")
    elif data.ultra_processed_ratio >= 0.25:
        score -= 5
    elif data.ultra_processed_ratio < 0.1:
        score += 4

    final = int(round(_clamp(score)))

    if not reasons:
        reasons.append("evenwichtige samenstelling")
    if final >= 75:
        prefix = "Gezond:"
    elif final >= 50:
        prefix = "Redelijk:"
    else:
        prefix = "Let op:"
    explanation = f"{prefix} {', '.join(reasons)}."

    # ontdubbel labels met behoud van volgorde
    seen: set[str] = set()
    dedup_labels: list[str] = []
    for label in labels:
        if label not in seen:
            dedup_labels.append(label)
            seen.add(label)

    return HealthScoreResult(score=final, explanation=explanation, labels=dedup_labels)


# Categorieen die we als 'ultrabewerkt' beschouwen voor de ratio
ULTRA_PROCESSED_CATEGORIES = {"spread", "wrap", "wraps", "snack", "frisdrank"}


def estimate_ultra_processed_ratio(ingredients_with_weight: list[tuple[str | None, float]]) -> float:
    total = sum(w for _, w in ingredients_with_weight) or 1.0
    upc = sum(w for cat, w in ingredients_with_weight if cat and cat.lower() in ULTRA_PROCESSED_CATEGORIES)
    return upc / total
