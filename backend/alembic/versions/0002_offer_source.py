"""offers.source kolom

Revision ID: 0002_offer_source
Revises: 0001_initial
Create Date: 2026-05-14 23:00:00

"""
from alembic import op
import sqlalchemy as sa


revision = "0002_offer_source"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "offers",
        sa.Column("source", sa.String(32), nullable=False, server_default="fallback_mock"),
    )
    op.create_index("ix_offers_source", "offers", ["source"])


def downgrade() -> None:
    op.drop_index("ix_offers_source", table_name="offers")
    op.drop_column("offers", "source")
