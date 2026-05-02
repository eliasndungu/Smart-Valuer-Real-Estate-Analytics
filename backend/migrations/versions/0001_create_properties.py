"""Create properties table

Revision ID: 0001_create_properties
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_create_properties"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "properties",
        sa.Column("id", sa.Integer(), nullable=False),

        # Source metadata
        sa.Column("source_site", sa.String(length=50), nullable=True),
        sa.Column("listing_url", sa.String(length=2048), nullable=False),
        sa.Column("scraped_at", sa.DateTime(), nullable=True),

        # Core listing attributes
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("price_period", sa.String(length=20), nullable=True),
        sa.Column("property_type", sa.String(length=50), nullable=True),

        # Location
        sa.Column("neighborhood", sa.String(length=256), nullable=True),
        sa.Column("county", sa.String(length=100), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),

        # Physical attributes
        sa.Column("bedrooms", sa.Integer(), nullable=True),
        sa.Column("bathrooms", sa.Integer(), nullable=True),
        sa.Column("size_sqft", sa.Float(), nullable=True),

        # Amenities / agent / description
        sa.Column("amenities", sa.Text(), nullable=True),
        sa.Column("agent_name", sa.String(length=256), nullable=True),
        sa.Column("agent_phone", sa.String(length=50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),

        # Record timestamps
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("listing_url", name="uq_properties_listing_url"),
    )

    # Indexes for common filter / join patterns
    op.create_index("ix_properties_id", "properties", ["id"], unique=False)
    op.create_index("ix_properties_source_site", "properties", ["source_site"], unique=False)
    op.create_index("ix_properties_property_type", "properties", ["property_type"], unique=False)
    op.create_index("ix_properties_neighborhood", "properties", ["neighborhood"], unique=False)
    op.create_index("ix_properties_county", "properties", ["county"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_properties_county", table_name="properties")
    op.drop_index("ix_properties_neighborhood", table_name="properties")
    op.drop_index("ix_properties_property_type", table_name="properties")
    op.drop_index("ix_properties_source_site", table_name="properties")
    op.drop_index("ix_properties_id", table_name="properties")
    op.drop_table("properties")
