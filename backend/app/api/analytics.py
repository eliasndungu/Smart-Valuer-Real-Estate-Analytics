"""
FastAPI router for analytics endpoints used by the dashboard.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.property import Property

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/avg-price-by-bedrooms", summary="Average price per bedroom count")
def avg_price_by_bedrooms(
    county: str | None = None,
    listing_type: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Return average property price grouped by number of bedrooms.
    Optionally filter by county and/or listing_type.
    """
    q = db.query(
        Property.bedrooms,
        func.avg(Property.price).label("avg_price"),
        func.count(Property.id).label("count"),
    ).filter(Property.is_active.is_(True), Property.bedrooms.isnot(None))

    if county:
        q = q.filter(func.lower(Property.county) == county.lower())
    if listing_type:
        q = q.filter(Property.price_period == listing_type)

    rows = q.group_by(Property.bedrooms).order_by(Property.bedrooms).all()

    return [
        {"bedrooms": r.bedrooms, "avg_price_kes": round(r.avg_price, 2), "count": r.count}
        for r in rows
    ]


@router.get("/neighborhood-trends", summary="Median price trends by neighbourhood")
def neighborhood_trends(
    county: str | None = None,
    listing_type: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Return average price and listing count grouped by neighbourhood,
    sorted descending by count.
    """
    q = db.query(
        Property.neighborhood,
        func.avg(Property.price).label("avg_price"),
        func.count(Property.id).label("listing_count"),
    ).filter(Property.is_active.is_(True), Property.neighborhood.isnot(None))

    if county:
        q = q.filter(func.lower(Property.county) == county.lower())
    if listing_type:
        q = q.filter(Property.price_period == listing_type)

    rows = (
        q.group_by(Property.neighborhood)
        .order_by(text("listing_count DESC"))
        .limit(limit)
        .all()
    )

    return [
        {
            "neighborhood": r.neighborhood,
            "avg_price_kes": round(r.avg_price, 2),
            "listing_count": r.listing_count,
        }
        for r in rows
    ]
