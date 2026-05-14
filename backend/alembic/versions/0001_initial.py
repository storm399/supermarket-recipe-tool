"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-14 00:00:00

"""
from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "supermarkets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("base_url", sa.String(255), nullable=True),
        sa.Column("logo_url", sa.String(255), nullable=True),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_supermarkets_slug", "supermarkets", ["slug"], unique=True)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("normalized_name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(128), nullable=True),
        sa.Column("unit", sa.String(64), nullable=True),
        sa.Column("amount", sa.Float, nullable=True),
        sa.Column("barcode", sa.String(64), nullable=True),
        sa.Column("image_url", sa.String(512), nullable=True),
    )
    op.create_index("ix_products_name", "products", ["name"])
    op.create_index("ix_products_normalized_name", "products", ["normalized_name"])

    op.create_table(
        "offers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("supermarket_id", sa.Integer, sa.ForeignKey("supermarkets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id", ondelete="SET NULL"), nullable=True),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(128), nullable=True),
        sa.Column("unit", sa.String(64), nullable=True),
        sa.Column("amount", sa.Float, nullable=True),
        sa.Column("original_price", sa.Float, nullable=True),
        sa.Column("sale_price", sa.Float, nullable=False),
        sa.Column("discount_percent", sa.Float, nullable=True),
        sa.Column("discount_text", sa.String(128), nullable=True),
        sa.Column("valid_from", sa.DateTime, nullable=True),
        sa.Column("valid_until", sa.DateTime, nullable=True),
        sa.Column("image_url", sa.String(512), nullable=True),
        sa.Column("source_url", sa.String(512), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("fetched_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_offers_supermarket_id", "offers", ["supermarket_id"])
    op.create_index("ix_offers_product_name", "offers", ["product_name"])

    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("instructions", sa.JSON, nullable=False),
        sa.Column("servings", sa.Integer, nullable=False),
        sa.Column("prep_time_minutes", sa.Integer, nullable=True),
        sa.Column("total_cost", sa.Float, nullable=True),
        sa.Column("cost_per_serving", sa.Float, nullable=True),
        sa.Column("diet_tags", sa.JSON, nullable=False),
        sa.Column("missing_pantry_items", sa.JSON, nullable=False),
        sa.Column("kcal_per_serving", sa.Float, nullable=True),
        sa.Column("protein_g", sa.Float, nullable=True),
        sa.Column("carbs_g", sa.Float, nullable=True),
        sa.Column("sugar_g", sa.Float, nullable=True),
        sa.Column("fat_g", sa.Float, nullable=True),
        sa.Column("saturated_fat_g", sa.Float, nullable=True),
        sa.Column("fiber_g", sa.Float, nullable=True),
        sa.Column("salt_g", sa.Float, nullable=True),
        sa.Column("nutrition_source", sa.String(64), nullable=True),
        sa.Column("health_score", sa.Integer, nullable=True),
        sa.Column("health_explanation", sa.Text, nullable=True),
        sa.Column("health_labels", sa.JSON, nullable=False),
        sa.Column("generated_by", sa.String(32), nullable=False, server_default="rule"),
        sa.Column("generated_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "recipe_ingredients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("recipe_id", sa.Integer, sa.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("offer_id", sa.Integer, sa.ForeignKey("offers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("quantity", sa.Float, nullable=True),
        sa.Column("unit", sa.String(64), nullable=True),
        sa.Column("is_pantry", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("estimated_cost", sa.Float, nullable=True),
        sa.Column("note", sa.String(255), nullable=True),
    )

    op.create_table(
        "nutrition_estimates",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("kcal_per_100", sa.Float, nullable=True),
        sa.Column("protein_per_100", sa.Float, nullable=True),
        sa.Column("carbs_per_100", sa.Float, nullable=True),
        sa.Column("sugar_per_100", sa.Float, nullable=True),
        sa.Column("fat_per_100", sa.Float, nullable=True),
        sa.Column("saturated_fat_per_100", sa.Float, nullable=True),
        sa.Column("fiber_per_100", sa.Float, nullable=True),
        sa.Column("salt_per_100", sa.Float, nullable=True),
        sa.Column("source", sa.String(64), nullable=False, server_default="fallback"),
        sa.Column("confidence", sa.String(32), nullable=False, server_default="estimated"),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("nutrition_estimates")
    op.drop_table("recipe_ingredients")
    op.drop_table("recipes")
    op.drop_index("ix_offers_product_name", table_name="offers")
    op.drop_index("ix_offers_supermarket_id", table_name="offers")
    op.drop_table("offers")
    op.drop_index("ix_products_normalized_name", table_name="products")
    op.drop_index("ix_products_name", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_supermarkets_slug", table_name="supermarkets")
    op.drop_table("supermarkets")
