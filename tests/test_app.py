import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from unittest.mock import patch
import pytest
from app import app
import data  # Import data module to reset state between tests


@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as client:
    yield client


@pytest.fixture(autouse=True)
def reset_products():
  """Resets the mock database array before each test to maintain test isolation."""
  data.products = [
      {
          "code": "3017620422003",
          "brand": "Nutella",
          "product_name": "Nutella",
          "key_ingredients": ["Sugar", "palm oil", "hazelnuts"],
          "categories": ["Spreads"],
          "allergens": ["Milk"],
          "nutritional_info_per_100g": {"energy_kcal": 539},
          "nutri_score": "E",
          "nova_group": 4,
      }
  ]


def test_get_inventory(client):
  response = client.get("/inventory")
  assert response.status_code == 200
  data = response.get_json()
  assert isinstance(data, list)
  assert data[0]["code"] == "3017620422003"


def test_get_inventory_by_code_local(client):
  response = client.get("/inventory/3017620422003")
  assert response.status_code == 200
  assert response.get_json()["brand"] == "Nutella"


def test_get_inventory_by_code_not_found(client):
  response = client.get("/inventory/9999999999999")
  assert response.status_code == 404
  assert "Product not found locally" in response.get_json()["message"]


@patch("app.requests.get")
def test_get_live_inventory_by_code_success(mock_get, client):
  # Mock the external OpenFoodFacts API response with the nested 'product' dictionary
  mock_response = mock_get.return_value
  mock_response.status_code = 200
  mock_response.json.return_value = {
      "product": {
          "code": "5449000000996",
          "brand": "Coca-Cola",
          "product_name": "Coke",
          "key_ingredients": ["Carbonated water", "sugar"],
      }
  }

  response = client.get("/inventory/api/code/5449000000996")
  assert response.status_code == 200
  data = response.get_json()
  assert data["code"] == "5449000000996"
  assert data["brand"] == "Coca-Cola"

@patch("app.requests.get")
def test_get_live_inventory_by_code_not_found(mock_get, client):
  mock_response = mock_get.return_value
  mock_response.status_code = 404

  response = client.get("/inventory/api/code/0000000000000")
  assert response.status_code == 404
  assert "Product not found in the API" in response.get_json()["message"]


def test_add_inventory_item(client):
  new_item = {"code": "1234567890123", "brand": "TestBrand", "product_name": "Test Item"}
  response = client.post("/inventory", json=new_item)
  assert response.status_code == 201
  assert response.get_json()["code"] == "1234567890123"


def test_add_inventory_item_missing_code(client):
  invalid_item = {"brand": "TestBrand"}
  response = client.post("/inventory", json=invalid_item)
  assert response.status_code == 400
  assert "code" in response.get_json()["message"]


def test_update_inventory_item(client):
  update_payload = {"product_name": "Updated Nutella Name"}
  response = client.patch("/inventory/3017620422003", json=update_payload)
  assert response.status_code == 200
  assert response.get_json()["product_name"] == "Updated Nutella Name"


def test_delete_inventory_item(client):
  response = client.delete("/inventory/3017620422003")
  assert response.status_code == 204

  # Confirm it's deleted
  check_response = client.get("/inventory/3017620422003")
  assert check_response.status_code == 404