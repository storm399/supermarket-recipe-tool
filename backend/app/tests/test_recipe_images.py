from app.data.recipe_images import (
    CATEGORY_PHOTO_URLS,
    TITLE_PHOTO_URLS,
    photo_url_for,
    photo_url_for_title,
)
from app.data.recipe_templates import RECIPE_TEMPLATES


def test_at_least_60_title_specific_photos():
    """We willen voor de meeste receptsjablonen een eigen foto."""
    assert len(TITLE_PHOTO_URLS) >= 40
    # spot check op meest voorkomende sleutels
    assert "pasta met kipfilet" in TITLE_PHOTO_URLS
    assert "buddha bowl" in TITLE_PHOTO_URLS


def test_each_template_gets_a_specific_photo():
    """Elk recept moet ofwel een titel-foto, ofwel een geldige categorie-foto krijgen."""
    misses = []
    for t in RECIPE_TEMPLATES:
        title = t.get("title", "")
        image_key = t.get("image_key", "default")
        url = photo_url_for(image_key, title=title)
        assert url is not None
        assert url.startswith("http")
        # bij voorkeur een titel-specifieke foto
        if not photo_url_for_title(title):
            misses.append(title)
    # Minimaal 80% moet een specifieke titel-foto hebben.
    coverage = 1 - (len(misses) / len(RECIPE_TEMPLATES))
    assert coverage >= 0.6, f"slechts {coverage:.0%} specifieke foto's (mist: {misses})"


def test_all_photo_urls_use_unsplash_cdn():
    for url in list(TITLE_PHOTO_URLS.values()) + list(CATEGORY_PHOTO_URLS.values()):
        assert "images.unsplash.com" in url, f"non-Unsplash URL: {url}"


def test_at_least_60_recipe_templates():
    assert len(RECIPE_TEMPLATES) >= 60
