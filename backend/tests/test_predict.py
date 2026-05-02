"""
Tests for the /predict endpoint and the prediction service.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health checks
# ---------------------------------------------------------------------------

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------------------------------------------------------------------------
# Prediction endpoint – happy paths
# ---------------------------------------------------------------------------

def test_predict_basic():
    payload = {
        "location": "Kilimani",
        "size_sqft": 1200,
        "bedrooms": 3,
        "bathrooms": 2,
        "property_type": "apartment",
        "listing_type": "sale",
        "amenities": ["parking"],
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price_kes"] > 0
    assert data["price_per_sqft_kes"] > 0
    assert data["confidence_interval"]["lower"] < data["predicted_price_kes"]
    assert data["confidence_interval"]["upper"] > data["predicted_price_kes"]
    assert "model_version" in data
    assert "placeholder" in data["disclaimer"].lower()


def test_predict_rent():
    payload = {
        "location": "Westlands",
        "size_sqft": 800,
        "bedrooms": 2,
        "listing_type": "rent",
        "amenities": [],
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Rent price should be significantly lower than sale price for same property
    assert data["predicted_price_kes"] > 0


def test_predict_unknown_location():
    payload = {
        "location": "Somewhere Unknown",
        "size_sqft": 500,
        "bedrooms": 1,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    # Should fall back to default price per sqft without error
    assert response.json()["predicted_price_kes"] > 0


def test_predict_with_premium_amenities():
    base_payload = {
        "location": "Karen",
        "size_sqft": 3000,
        "bedrooms": 5,
        "amenities": [],
    }
    premium_payload = {**base_payload, "amenities": ["swimming pool", "gym", "generator"]}

    base_response = client.post("/predict", json=base_payload).json()
    premium_response = client.post("/predict", json=premium_payload).json()

    # Adding premium amenities must increase the predicted price
    assert premium_response["predicted_price_kes"] > base_response["predicted_price_kes"]


# ---------------------------------------------------------------------------
# Prediction endpoint – validation errors
# ---------------------------------------------------------------------------

def test_predict_missing_location():
    payload = {"size_sqft": 1000, "bedrooms": 2}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_negative_size():
    payload = {"location": "Kilimani", "size_sqft": -100, "bedrooms": 2}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_property_type():
    payload = {
        "location": "Kilimani",
        "size_sqft": 1000,
        "bedrooms": 2,
        "property_type": "castle",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
