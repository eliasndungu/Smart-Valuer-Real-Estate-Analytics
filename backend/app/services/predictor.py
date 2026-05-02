"""
Placeholder price-prediction service.

In production this module should:
  1. Load a trained scikit-learn pipeline from disk (e.g. joblib / pickle).
  2. Transform the input features using the same preprocessor used during training.
  3. Return the model's prediction and, if available, a calibrated confidence interval.

For now it uses a rule-based heuristic so the API is fully functional end-to-end
without requiring a trained model artifact.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.prediction import PropertyFeatures

logger = logging.getLogger(__name__)

MODEL_VERSION = "placeholder-v0.1.0"

# ---------------------------------------------------------------------------
# Base price per square foot by neighbourhood tier (KES)
# ---------------------------------------------------------------------------
_NEIGHBOURHOOD_TIER: dict[str, float] = {
    # Premium Nairobi suburbs
    "karen": 18_000,
    "lavington": 16_500,
    "muthaiga": 20_000,
    "runda": 19_000,
    "kitisuru": 17_500,
    "gigiri": 18_500,
    # Upper-mid Nairobi
    "kilimani": 14_000,
    "westlands": 13_500,
    "kileleshwa": 13_000,
    "parklands": 12_500,
    "spring valley": 14_500,
    "lower kabete": 11_000,
    # Mid Nairobi
    "south b": 9_000,
    "south c": 9_000,
    "langata": 8_500,
    "embakasi": 7_000,
    "donholm": 7_500,
    "ruaka": 8_000,
    "thika road": 7_000,
    # Satellite towns
    "ruiru": 5_500,
    "athi river": 5_000,
    "kitengela": 4_500,
    "ngong": 5_000,
    "limuru": 6_000,
    # Other counties
    "mombasa": 7_000,
    "nyali": 9_500,
    "kisumu": 5_000,
    "nakuru": 5_500,
    "eldoret": 5_000,
}
_DEFAULT_PRICE_PER_SQFT = 8_000  # fallback for unknown neighbourhoods

# Bedroom premium multipliers
_BEDROOM_MULTIPLIER: dict[int, float] = {
    0: 0.70,  # studio
    1: 0.85,
    2: 0.95,
    3: 1.00,
    4: 1.08,
    5: 1.15,
}

# Amenity value additions (KES per amenity)
_AMENITY_VALUES: dict[str, float] = {
    "swimming pool": 2_000_000,
    "pool": 2_000_000,
    "gym": 500_000,
    "borehole": 800_000,
    "solar": 600_000,
    "generator": 700_000,
    "backup generator": 700_000,
    "cctv": 200_000,
    "parking": 500_000,
    "lift": 300_000,
    "elevator": 300_000,
    "servant quarters": 800_000,
    "dsq": 800_000,
    "garden": 400_000,
    "balcony": 200_000,
}


def predict_price(features: "PropertyFeatures") -> dict:
    """
    Return a dummy price prediction dict for the given property features.

    Replace this function body with a real model.load() + model.predict() call.
    """
    location_key = features.location.lower().strip()
    price_per_sqft = _NEIGHBOURHOOD_TIER.get(location_key, _DEFAULT_PRICE_PER_SQFT)

    # Bedroom adjustment
    bedroom_mult = _BEDROOM_MULTIPLIER.get(features.bedrooms, 1.10)

    # Base price
    base_price = features.size_sqft * price_per_sqft * bedroom_mult

    # Rent vs sale adjustment
    if features.listing_type.value == "rent":
        base_price = base_price * 0.006  # rough monthly rent ≈ 0.6 % of asset value

    # Amenity add-ons
    amenity_bonus = 0.0
    for amenity in features.amenities:
        amenity_bonus += _AMENITY_VALUES.get(amenity.lower().strip(), 50_000)

    predicted_price = base_price + amenity_bonus

    # Fake ±15% confidence interval
    margin = predicted_price * 0.15
    price_per_sqft_result = predicted_price / features.size_sqft if features.size_sqft else 0.0

    logger.debug(
        "Prediction: location=%s size=%.0f beds=%d → KES %.0f",
        features.location,
        features.size_sqft,
        features.bedrooms,
        predicted_price,
    )

    return {
        "predicted_price_kes": round(predicted_price, 2),
        "price_per_sqft_kes": round(price_per_sqft_result, 2),
        "confidence_interval": {
            "lower": round(predicted_price - margin, 2),
            "upper": round(predicted_price + margin, 2),
        },
        "model_version": MODEL_VERSION,
    }
