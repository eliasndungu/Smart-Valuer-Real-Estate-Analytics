"""
FastAPI router for the /predict endpoint.
"""

from fastapi import APIRouter

from app.schemas.prediction import PropertyFeatures, PricePredictionResponse
from app.services.predictor import predict_price

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post(
    "",
    response_model=PricePredictionResponse,
    summary="Predict property price",
    description=(
        "Accepts property features (location, size, bedrooms, amenities, etc.) "
        "and returns a price estimate in Kenyan Shillings (KES). "
        "The current implementation uses a placeholder model – "
        "replace `app.services.predictor.predict_price` with a trained model."
    ),
)
def predict(features: PropertyFeatures) -> PricePredictionResponse:
    result = predict_price(features)
    return PricePredictionResponse(**result)
