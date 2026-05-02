"""
SQLAlchemy ORM model for the Properties table.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Property(Base):
    """Persisted property listing record."""

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)

    # Source
    source_site = Column(String(50), nullable=True, index=True)
    listing_url = Column(String(2048), unique=True, nullable=False)
    scraped_at = Column(DateTime, nullable=True)

    # Core attributes
    title = Column(String(512), nullable=True)
    price = Column(Float, nullable=False)
    price_period = Column(String(20), nullable=True)   # "sale" | "monthly" | "daily"
    property_type = Column(String(50), nullable=True, index=True)

    # Location
    neighborhood = Column(String(256), nullable=True, index=True)
    county = Column(String(100), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Physical attributes
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    size_sqft = Column(Float, nullable=True)

    # Amenities stored as comma-separated string for simplicity
    amenities = Column(Text, nullable=True)

    # Agent info
    agent_name = Column(String(256), nullable=True)
    agent_phone = Column(String(50), nullable=True)

    # Raw text
    description = Column(Text, nullable=True)

    # Record timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Property id={self.id} type={self.property_type!r} "
            f"neighborhood={self.neighborhood!r} price={self.price}>"
        )
