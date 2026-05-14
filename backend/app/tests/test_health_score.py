from app.services.health_score import (
    HealthScoreInput,
    compute_health_score,
    estimate_ultra_processed_ratio,
)


def test_score_is_clamped_between_0_and_100():
    result = compute_health_score(
        HealthScoreInput(
            kcal_per_serving=2000,
            protein_g=0,
            fiber_g=0,
            saturated_fat_g=50,
            salt_g=10,
            sugar_g=100,
        )
    )
    assert 0 <= result.score <= 100


def test_healthy_meal_scores_high():
    result = compute_health_score(
        HealthScoreInput(
            kcal_per_serving=450,
            protein_g=30,
            fiber_g=10,
            saturated_fat_g=2,
            salt_g=0.8,
            sugar_g=4,
            veg_fruit_grams_per_serving=300,
            ultra_processed_ratio=0.0,
        )
    )
    assert result.score >= 75
    assert "eiwitrijk" in result.labels
    assert "vezelrijk" in result.labels


def test_unhealthy_meal_scores_low():
    result = compute_health_score(
        HealthScoreInput(
            kcal_per_serving=900,
            protein_g=5,
            fiber_g=1,
            saturated_fat_g=15,
            salt_g=4,
            sugar_g=30,
            veg_fruit_grams_per_serving=10,
            ultra_processed_ratio=0.6,
        )
    )
    assert result.score < 40
    assert "veel zout" in result.labels
    assert "veel suiker" in result.labels


def test_explanation_not_empty():
    result = compute_health_score(
        HealthScoreInput(
            kcal_per_serving=500,
            protein_g=20,
            fiber_g=5,
            saturated_fat_g=4,
            salt_g=1.5,
            sugar_g=10,
        )
    )
    assert isinstance(result.explanation, str)
    assert len(result.explanation) > 0


def test_ultra_processed_ratio():
    weighted = [("groente", 200.0), ("spread", 100.0), ("zuivel", 100.0)]
    ratio = estimate_ultra_processed_ratio(weighted)
    assert 0.24 < ratio < 0.26
